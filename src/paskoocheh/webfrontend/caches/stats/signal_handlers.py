# coding: utf-8
# Paskoocheh - A tool marketplace for Iranian
#
# Copyright (C) 2024 ASL19 Organization
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

u"""webfrontend stats cache signal handlers."""

import logging
import math
from collections import defaultdict
from django.core.cache import cache
from stats.models import VersionDownload, VersionRating
from webfrontend.caches.utils import (
    cache_key_data_to_cache_key,
    delete_cached_responses_matching_patterns,
)

logger = logging.getLogger(__name__)


# ========================
# === Helper functions ===
# ========================
def get_normalized_platform_slug_name(slug_name):
    """
    Normalize a slug_name.

    This is necessary because 32-bit and 64-bit Linux/Windows stats are tracked
    independently, but are displayed as an aggregate. It’s also useful for
    normalizing old iterations of the Linux slug_name.

    Args:
        slug_name (str): Platform.slug_name
    """
    if slug_name in ['linux32', 'linux_32', 'linux64', 'linux_64']:
        return 'linux'
    elif slug_name in ['windows32', 'windows64']:
        return 'windows'

    return slug_name


def get_tool_id_platform_key(versiondownload):
    """
    Given a versiondownload object, return a
    "{tool_id}_{platform_slug_name}" key.

    This key format is exclusively used within the stats cache for download
    count aggregation.

    Args:
        versiondownload (VersionDownload)

    Returns:
        unicode
    """
    return u'{tool_id}_{platform_slug_name}'.format(
        tool_id=versiondownload.tool_id,
        platform_slug_name=(
            get_normalized_platform_slug_name(versiondownload.platform_name)
        ),
    )


# =======================
# === Signal handlers ===
# =======================
def update_versiondownload_cache_values(sender, **kwargs):
    """
    Update versiondownload stats cache values (signal receiver).

    Gets all VersionDownload objects, aggregates download totals, and
    writes values to cache. Overwrites existing data.
    """
    logger.info(u'VersionDownload post_batch_update signal recieved')

    versiondownloads = VersionDownload.objects.all()

    downloads_by_tool_id = {}
    downloads_by_tool_id_platform = {}

    for versiondownload in versiondownloads:
        versiondownload.id_platform_key = get_tool_id_platform_key(versiondownload)

        if versiondownload.id_platform_key in downloads_by_tool_id_platform:
            downloads_by_tool_id_platform[versiondownload.id_platform_key] += versiondownload.download_count
        else:
            downloads_by_tool_id_platform[versiondownload.id_platform_key] = versiondownload.download_count

        if versiondownload.tool_id in downloads_by_tool_id:
            downloads_by_tool_id[versiondownload.tool_id] += versiondownload.download_count
        else:
            downloads_by_tool_id[versiondownload.tool_id] = versiondownload.download_count

    cache_data = {}

    for versiondownload in versiondownloads:
        cache_key = cache_key_data_to_cache_key({
            u'cache_type': u'stat_versiondownload',
            u'tool_id': versiondownload.tool_id,
            u'platform_slug_name': (
                get_normalized_platform_slug_name(versiondownload.platform_name)
            )
        })

        if cache_key not in cache_data:
            cache_data[cache_key] = downloads_by_tool_id_platform[versiondownload.id_platform_key]

    for tool_id in downloads_by_tool_id:
        cache_key = cache_key_data_to_cache_key({
            u'cache_type': u'stat_versiondownload',
            u'tool_id': tool_id,
            u'platform_slug_name': 'all'
        })

        cache_data[cache_key] = downloads_by_tool_id[tool_id]

    cache.set_many(cache_data, None)


def update_versionrating_cache_values(sender, **kwargs):
    """
    Update versionrating and versionrating_count stats cache values (signal
    receiver).

    Gets all VersionRating objects; writes all versionrating and
    versionrating_count values to cache. Overwrites existing data.
    """
    logger.info(u'VersionRating post_batch_update signal recieved')

    cache_data = {}

    versionratings = VersionRating.objects.all()

    total_rating_by_tool_id = defaultdict(float)
    total_rating_count_by_tool_id = defaultdict(int)

    for versionrating in versionratings:
        versionrating_cache_key = cache_key_data_to_cache_key({
            u'cache_type': u'stat_versionrating',
            u'tool_id': versionrating.tool_id,
            u'platform_slug_name': versionrating.platform_name,
        })

        cache_data[versionrating_cache_key] = versionrating.star_rating

        versionrating_count_cache_key = cache_key_data_to_cache_key({
            u'cache_type': u'stat_versionrating_count',
            u'tool_id': versionrating.tool_id,
            u'platform_slug_name': versionrating.platform_name,
        })

        cache_data[versionrating_count_cache_key] = versionrating.rating_count

        total_rating_by_tool_id[versionrating.tool.id] += (
            float(versionrating.star_rating * versionrating.rating_count)
        )
        total_rating_count_by_tool_id[versionrating.tool.id] += (
            int(versionrating.rating_count)
        )

    for tool_id in total_rating_by_tool_id:
        versionrating_cache_key = cache_key_data_to_cache_key({
            u'cache_type': u'stat_versionrating',
            u'tool_id': tool_id,
            u'platform_slug_name': 'all',
        })

        average_rating = (
            total_rating_by_tool_id[tool_id] / total_rating_count_by_tool_id[tool_id]
        )

        average_rating_1_decimal_floor = (
            '{:.1f}'.format(
                math.floor(average_rating * 10) / 10
            )
        )

        cache_data[versionrating_cache_key] = average_rating_1_decimal_floor

        versionrating_count_cache_key = cache_key_data_to_cache_key({
            u'cache_type': u'stat_versionrating_count',
            u'tool_id': tool_id,
            u'platform_slug_name': 'all',
        })

        cache_data[versionrating_count_cache_key] = total_rating_count_by_tool_id[tool_id]

    cache.set_many(cache_data, None)

    purge_index_and_search()


def purge_index_and_search():
    logger.info(u'purge_index_and_search')

    delete_cached_responses_matching_patterns(
        {
            u'url_name': u'index'
        }, {
            u'url_name': u'search'
        },
    )
