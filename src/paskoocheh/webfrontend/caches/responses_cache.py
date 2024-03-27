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

u"""webfrontend responses cache."""

import logging
from blog.models import Category, Comment, Post
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.utils.decorators import method_decorator
from django.core.cache import cache
from fancy_cache import cache_page
from preferences.models import Platform, PromoImage, Text, ToolType
from stats.models import VersionReview
from tools.models import Faq, Guide, Info, Tool, Tutorial, Version
from webfrontend.caches.utils import (
    cache_key_data_to_cache_key,
    pattern_dict_to_pattern_glob,
)
from webfrontend.utils import is_request_user_agent_noop

logger = logging.getLogger(__name__)


# =======================
# === Cache decorator ===
# =======================
def get_cache_key_prefix(request):
    # Data included in every key
    cache_key_data = {
        u'cache_type': u'response',
        u'global_platform_slug': request.global_version_slug,
        u'is_noop': str(is_request_user_agent_noop(request)).lower(),
        u'url_name': request.resolver_match.url_name,
    }

    # Add path arguments (urls.py named groups)
    for key in request.resolver_match.kwargs:
        if key != u'path_prefix':
            cache_key_data_key = u'p_{key}'.format(key=key)
            cache_key_data[cache_key_data_key] = request.resolver_match.kwargs[key]

    # Add query (GET) arguments
    for key in request.GET:
        cache_key_data_key = u'q_{key}'.format(key=key)
        cache_key_data[cache_key_data_key] = request.GET[key]

    # Compile cache key
    cache_key_prefix = cache_key_data_to_cache_key(cache_key_data)

    return cache_key_prefix


def pk_cache_response(timeout=settings.WEBFRONTEND_CACHE_RESPONSE_TIMEOUT):
    if settings.WEBFRONTEND_CACHE_RESPONSE_ENABLED:
        return method_decorator(
            cache_page(
                timeout,
                key_prefix=get_cache_key_prefix,
            )
        )
    else:
        return lambda function: function


# =====================
# === Cache manager ===
# =====================
# Instance created in WebfrontendConfig.ready

class ResponsesCacheManager(object):
    u"""
    Purges response caches in response to model save/delete signals.

    The purpose of this is to ensure that all cached responses that include a
    backend entity are purged when that entity is modified or removed. The
    caching strategy is built around responses being cached indefinitely, so
    it’s very important that all potential cases are covered.
    """
    def __init__(self):
        self.register_signal_receivers()

    # ========================================
    # === Cache deletion utility functions ===
    # ========================================
    def delete_keys_matching_pattern(self, delete_pattern_dict):
        """
        Delete all keys matching a dict pattern.

        Args:
            delete_pattern_dict (dict): Dictionary describing keys to delete
                (app_name and app_version are added automatically)

        Returns:
            None
        """
        delete_pattern_dict = delete_pattern_dict.copy()
        delete_pattern_dict[u'cache_type'] = u'response'

        cache.delete_pattern(
            pattern_dict_to_pattern_glob(delete_pattern_dict)
        )

    def delete_cached_responses_matching_patterns(self, *delete_pattern_dicts):
        """
        Delete all keys matching provided dict patterns.

        Args:
            delete_pattern_dicts (dict): Dictionaries describing keys to delete
                (app_name and app_version are added automatically)

        Returns:
            None
        """
        for delete_pattern_dict in delete_pattern_dicts:
            self.delete_keys_matching_pattern(delete_pattern_dict)

    # ======================================
    # === Cache invalidation via signals ===
    # ======================================

    def purge_all(self, sender, **kwargs):
        logger.debug(u'purge_all')
        self.delete_keys_matching_pattern({u'cache_type': u'response'})

    def purge_blog(self, sender, **kwargs):
        logger.debug(u'purge_blog')

        self.delete_cached_responses_matching_patterns(
            {
                u'url_name': u'blogindex'
            },
            {
                u'url_name': u'blogpost'
            },
            {
                u'url_name': u'blogposts'
            },
            {
                u'url_name': u'blogpostsfeed'
            },
            {
                u'url_name': u'toolversion'
            },
        )

    def purge_faq(self, sender, **kwargs):
        logger.debug('purge_faq')

        # Don’t invalidate caches if only the click_count field has changed
        if ('update_fields' in kwargs and type(kwargs['update_fields']) == frozenset and 'click_count' in kwargs['update_fields']):
            logger.debug(u'FAQ click_count changed – NOT invalidating affected cached responses')
            return

        logger.debug(u'FAQ changed – invalidating affected cached responses')

        tool_id = kwargs['instance'].tool_id

        self.delete_cached_responses_matching_patterns(
            {
                u'url_name': u'toolfaq',
                u'p_tool_id': tool_id
            }, {
                u'url_name': u'toolfaqs',
                u'p_tool_id': tool_id
            }, {
                u'url_name': u'toolversion',
                u'p_tool_id': tool_id
            }, {
                u'url_name': u'toolversionfaq',
                u'p_tool_id': tool_id
            }, {
                u'url_name': u'toolversionfaqs',
                u'p_tool_id': tool_id
            },
        )

    def purge_guide(self, sender, **kwargs):
        logger.debug(u'purge_guide')

        tool_id = kwargs['instance'].version.tool.id
        version_slug = kwargs['instance'].version.supported_os.slug_name

        self.delete_cached_responses_matching_patterns(
            {
                u'url_name': u'toolversion',
                u'p_tool_id': tool_id,
                u'p_version_slug': version_slug,
            }, {
                u'url_name': u'toolversionguide',
                u'p_tool_id': tool_id,
                u'p_version_slug': version_slug,
            },
        )

    def purge_index(self, sender, **kwargs):
        logger.debug(u'purge_index')

        self.delete_cached_responses_matching_patterns(
            {
                u'url_name': u'index'
            },
        )

    def purge_info_tool_version(self, sender, **kwargs):
        logger.debug(u'purge_info_tool_version')

        if sender in [Info, Version]:
            tool_id = kwargs['instance'].tool_id
        elif sender is Tool:
            tool_id = kwargs['instance'].id

        self.delete_cached_responses_matching_patterns(
            {
                u'url_name': u'index'
            }, {
                u'url_name': u'search'
            }, {
                u'url_name': u'toolfaq',
                u'p_tool_id': tool_id,
            }, {
                u'url_name': u'toolfaqs',
                u'p_tool_id': tool_id,
            }, {
                u'url_name': u'toolversion',
                u'p_tool_id': tool_id,
            }, {
                u'url_name': u'toolversionfaq',
                u'p_tool_id': tool_id,
            }, {
                u'url_name': u'toolversionfaqs',
                u'p_tool_id': tool_id,
            }, {
                u'url_name': u'toolversionguide',
                u'p_tool_id': tool_id,
            }, {
                u'url_name': u'toolversiontutorial',
                u'p_tool_id': tool_id,
            }, {
                u'url_name': u'toolversiontutorials',
                u'p_tool_id': tool_id,
            }, {
                u'url_name': u'toolversionreview',
                u'p_tool_id': tool_id,
            }, {
                u'url_name': u'toolversionreviews',
                u'p_tool_id': tool_id,
            },
        )

    def purge_pages(self, sender, **kwargs):
        logger.debug(u'purge_pages')

        self.delete_cached_responses_matching_patterns(
            {
                u'url_name': u'page'
            },
        )

    def purge_tutorial(self, sender, **kwargs):
        logger.debug(u'purge_tutorial')

        tool_id = kwargs['instance'].version.tool.id
        version_slug = kwargs['instance'].version.supported_os.slug_name

        self.delete_cached_responses_matching_patterns(
            {
                u'url_name': u'toolversion',
                u'p_tool_id': tool_id,
                u'p_version_slug': version_slug,
            }, {
                u'url_name': u'toolversiontutorial',
                u'p_tool_id': tool_id,
                u'p_version_slug': version_slug,
            }, {
                u'url_name': u'toolversiontutorials',
                u'p_tool_id': tool_id,
                u'p_version_slug': version_slug,
            },
        )

    def purge_versionreview(self, sender, **kwargs):
        logger.debug(u'delete_for_versionreview')

        tool_id = kwargs.get('instance').tool_id
        version_slug = kwargs.get('instance').platform_name
        versionreview_id = kwargs.get('instance').id

        self.delete_cached_responses_matching_patterns(
            {
                u'url_name': u'toolversion',
                u'p_tool_id': tool_id,
                u'p_version_slug': version_slug,
            }, {
                u'url_name': u'toolversionreview',
                u'p_tool_id': tool_id,
                u'p_version_slug': version_slug,
                u'p_review_id': versionreview_id,
            }, {
                u'url_name': u'toolversionreviews',
                u'p_tool_id': tool_id,
                u'p_version_slug': version_slug
            },
        )

    def register_signal_receivers(self):
        logger.info(u'Registering signal receivers')

        for signal in [post_delete, post_save]:
            for sender in [Platform, ToolType]:
                signal.connect(self.purge_all, sender=sender, weak=False)

            for sender in [Category, Comment, Post]:
                signal.connect(self.purge_blog, sender=sender, weak=False)

            signal.connect(self.purge_faq, sender=Faq, weak=False)

            signal.connect(self.purge_guide, sender=Guide, weak=False)

            signal.connect(self.purge_index, sender=PromoImage, weak=False)

            for sender in [Info, Tool, Version]:
                signal.connect(self.purge_info_tool_version, sender=sender, weak=False)

            signal.connect(self.purge_pages, sender=Text, weak=False)

            signal.connect(self.purge_tutorial, sender=Tutorial, weak=False)

            signal.connect(self.purge_versionreview, sender=VersionReview, weak=False)
