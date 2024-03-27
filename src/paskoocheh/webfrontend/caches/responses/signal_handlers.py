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

u"""webfrontend responses cache signal handlers."""

import logging
from paskoocheh.helpers import disable_for_loaddata
from webfrontend.caches.utils import (
    delete_cached_responses_matching_patterns,
    delete_keys_matching_pattern,
)

logger = logging.getLogger(__name__)


# ==========================================
# === Cache invalidation signal handlers ===
# ==========================================
# Registered at bottom of file.

@disable_for_loaddata
def purge_all(sender, **kwargs):
    logger.info(u'purge_all')
    delete_keys_matching_pattern({u'cache_type': u'response'})


@disable_for_loaddata
def purge_blog(sender, **kwargs):
    logger.info(u'purge_blog')

    delete_cached_responses_matching_patterns(
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


@disable_for_loaddata
def purge_faq(sender, **kwargs):
    logger.info('purge_faq')

    # Don’t invalidate caches if only the click_count field has changed
    if (
        'update_fields' in kwargs and
        type(kwargs['update_fields']) == frozenset and
        'click_count' in kwargs['update_fields']
    ):
        logger.debug(u'FAQ click_count changed – NOT invalidating affected cached responses')
        return

    logger.debug(u'FAQ changed – invalidating affected cached responses')

    tool_id = kwargs['instance'].tool_id

    delete_cached_responses_matching_patterns(
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


@disable_for_loaddata
def purge_guide(sender, **kwargs):
    logger.info(u'purge_guide')

    tool_id = kwargs['instance'].version.tool.id
    platform_slug = kwargs['instance'].version.supported_os.slug_name

    delete_cached_responses_matching_patterns(
        {
            u'url_name': u'toolversion',
            u'p_tool_id': tool_id,
            u'p_platform_slug': platform_slug,
        }, {
            u'url_name': u'toolversionguide',
            u'p_tool_id': tool_id,
            u'p_platform_slug': platform_slug,
        },
    )


@disable_for_loaddata
def purge_index(sender, **kwargs):
    logger.info(u'purge_index')

    delete_cached_responses_matching_patterns(
        {
            u'url_name': u'index'
        },
    )


@disable_for_loaddata
def purge_info_tool_version(sender, **kwargs):
    from tools.models import Info, Tool, Version, VersionCode

    logger.info(u'purge_info_tool_version')

    if sender in [Info, Version]:
        tool_id = kwargs['instance'].tool_id
    elif sender is Tool:
        tool_id = kwargs['instance'].id
    elif sender is VersionCode:
        tool_id = kwargs['instance'].version.tool_id

    delete_cached_responses_matching_patterns(
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


@disable_for_loaddata
def purge_pages(sender, **kwargs):
    logger.info(u'purge_pages')

    delete_cached_responses_matching_patterns(
        {
            u'url_name': u'page'
        },
    )


@disable_for_loaddata
def purge_tutorial(sender, **kwargs):
    logger.info(u'purge_tutorial')

    tool_id = kwargs['instance'].version.tool.id
    platform_slug = kwargs['instance'].version.supported_os.slug_name

    delete_cached_responses_matching_patterns(
        {
            u'url_name': u'toolversion',
            u'p_tool_id': tool_id,
            u'p_platform_slug': platform_slug,
        }, {
            u'url_name': u'toolversiontutorial',
            u'p_tool_id': tool_id,
            u'p_platform_slug': platform_slug,
        }, {
            u'url_name': u'toolversiontutorials',
            u'p_tool_id': tool_id,
            u'p_platform_slug': platform_slug,
        },
    )


@disable_for_loaddata
def purge_versionreview(sender, **kwargs):
    logger.info(u'purge_versionreview')

    tool_id = kwargs.get('instance').tool_id
    platform_slug = kwargs.get('instance').platform_name
    versionreview_id = kwargs.get('instance').id

    delete_cached_responses_matching_patterns(
        {
            u'url_name': u'toolversion',
            u'p_tool_id': tool_id,
            u'p_platform_slug': platform_slug,
        }, {
            u'url_name': u'toolversionreview',
            u'p_tool_id': tool_id,
            u'p_platform_slug': platform_slug,
            u'p_review_id': versionreview_id,
        }, {
            u'url_name': u'toolversionreviews',
            u'p_tool_id': tool_id,
            u'p_platform_slug': platform_slug
        },
    )
