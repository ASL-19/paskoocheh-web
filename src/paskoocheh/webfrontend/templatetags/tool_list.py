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

u"""Registers webfrontend’s custom Django template tags."""

import icu
from django import template
from operator import attrgetter
from webfrontend.templatetags.tool_list_item import ToolListItemContext
from webfrontend.utils.general import enforce_required_args
from django.conf import settings

register = template.Library()

app = settings.PLATFORM


@register.inclusion_tag('webfrontend/tags/tool_list.html')
def tool_list(tool_list_item_contexts, is_preview=False, in_search_view=False):
    return {
        'tool_list_item_contexts': tool_list_item_contexts,
        'is_preview': is_preview,
        'in_search_view': in_search_view,
    }


def construct_tool_list_item_context_list(  # noqa: C901
    order_by=None,
    order_reverse=False,
    request=None,
    stats_for_platform_slug_name=None,
    tools=None,
):
    u"""
    Processes a list of tools into a list of ToolListItemContext ordered by
    order_by, or by transliterated name if no order provided.

    Required args:
        request (WSGIRequest)
        stats_for_platform_slug_name (str): Platform name to use when querying
            stats. To get aggregate stats, use “all”. Affects displayed stats
            as well as download_count ordering.
        tools (iterable of Tool)

    Optional args:
        order_by (str): ToolListItemContext sorting key
        order_reverse (bool): Reverse sorting order?

    Returns:
        list of ToolListItemContext
    """
    enforce_required_args(locals(), 'request', 'stats_for_platform_slug_name', 'tools')

    # =============================================
    # === Build list of tool_list_item_context  ===
    # =============================================
    tool_list_item_contexts = []

    for tool in tools:
        # Don’t include tool if it isn’t publishable or has no (publishable)
        # versions
        if tool.publishable is False or tool.versions.count() == 0:
            continue

        # tool.logo_images is populated by prefetch_related in the main view
        if (
            hasattr(tool, 'logo_images') and
            len(tool.logo_images) > 0
        ):
            logo = tool.logo_images[0].image.url
        else:
            logo = settings.WEBFRONTEND_DEFAULT_IMAGE_PATH

        # To get the first tool version (which is the one we display, since the
        # list is preferentially ordered in the query), it’s faster to use
        # tool.versions.all()[0] rather than tool.versions.first() because the
        # result of .all() is already prefetched in memory.
        version = tool.versions.all()[0]

        # -----------------------------------------------------------------
        # --- Figure out if a browser version badge should be displayed ---
        # -----------------------------------------------------------------
        current_view_name = request.resolver_match.url_name

        should_display_browser_badge = (
            current_view_name in ['index', 'search'] and
            version.supported_os.slug_name in ['chrome', 'firefox'] and
            'platform' in request.GET and
            request.GET['platform'] in ['linux', 'macos', 'windows']
        )

        # ---------------------
        # --- Get tool name ---
        # ---------------------
        tool_info = None
        if (
            hasattr(tool, 'infos_current_language') and
            len(tool.infos_current_language) > 0
        ):
            tool_info = tool.infos_current_language[0]

        if tool_info is not None:
            name = tool_info.name
        else:
            name = tool.name

        should_display_all_platform_stats = (
            stats_for_platform_slug_name == 'all'
        )

        # ---------------------------------------------------
        # --- Find version download count in cache values ---
        # ---------------------------------------------------
        download_count = 0
        for key in request.webfrontend_stats['versiondownload_values_by_key']:
            if (
                'tool_id={}&'.format(tool.id) in key and
                'platform_slug_name={}&'.format('all' if should_display_all_platform_stats else version.supported_os.slug_name) in key
            ):
                download_count = int(request.webfrontend_stats['versiondownload_values_by_key'][key])
                break

        in_search_view = ('query' in request.GET)

        # ----------------------------------------
        # --- Construct tool list item context ---
        # ----------------------------------------
        tool_list_item_contexts.append(
            ToolListItemContext(
                download_count=download_count,
                logo=logo,
                name=name,
                platform_slug=version.supported_os.slug_name,
                should_display_browser_badge=should_display_browser_badge,
                should_display_all_platform_stats=should_display_all_platform_stats,
                version=version,
                in_search_view=in_search_view,
            )
        )

    if order_by:
        sorted_tool_list_item_contexts = (
            sorted(
                tool_list_item_contexts,
                key=attrgetter(order_by),
                reverse=order_reverse
            )
        )
    else:
        icu_transliterator = icu.Transliterator.createInstance('Arabic-Latin/BGN' if app == 'zanga' else 'Persian-Latin/BGN')

        sorted_tool_list_item_contexts = (
            sorted(
                tool_list_item_contexts,
                key=lambda tool_list_item: icu_transliterator.transliterate(tool_list_item.name)
            )
        )

    return sorted_tool_list_item_contexts
