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

u"""webfrontend tool list utilities."""

import re
from django.utils.translation import pgettext
from django.utils import translation


def get_tool_list_title(**kwargs):
    u"""
    Returns a translated tool list title based on the provided kwargs.

    Args:
        **kwargs:
            is_featured (bool): True if list is limited to featured tools
            is_for_other_platforms (bool): True if the list contains tools for
                other platforms (used in SearchView)
            order_by_slug (str): Slug code describing order of list (same as
                `orderby` SearchView GET argument)
            platform_locale_display_name (str): Platform display name (translated)
            query (str): Raw search query

    Returns:
        Unicode string
    """

    # ===================
    # === Read kwargs ===
    # ===================

    is_featured = kwargs.get('is_featured', False)
    is_for_other_platforms = kwargs.get('is_for_other_platforms', False)
    order_by_slug = kwargs.get('order_by_slug', None)
    platform_locale_display_name = kwargs.get('platform_locale_display_name', None)
    query = kwargs.get('query', None)
    tool_type_name = kwargs.get('tool_type_name', None)
    requires_article_prefix = kwargs.get('requires_article_prefix', None)

    # ==========================
    # === Gather format args ===
    # ==========================

    featured_translation = None
    if is_featured:
        featured_translation = pgettext(
            u'List title',
            # Translators: Feeds into blog/tool list title {featured} fields
            u'Featured'
        )

    description_translation = None
    if order_by_slug:
        if order_by_slug == u'downloadcount':
            description_translation = pgettext(
                u'Tool list title description',
                # Translators: Used in tool list titles on homepage, category
                # pages, and search pages. Feeds into tool list title
                # {description} fields.
                u'Most downloaded'
            )
        elif order_by_slug == u'dateadded':
            description_translation = pgettext(
                u'Tool list title description',
                # Translators: Used in tool list titles on homepage, category
                # pages, and search pages. Feeds into tool list title
                # {description} fields.
                u'Recently added'
            )
        elif order_by_slug == u'dateupdated':
            description_translation = pgettext(
                u'Tool list title description',
                # Translators: Used in tool list titles on homepage, category
                # pages, and search pages. Feeds into tool list title
                # {description} fields.
                u'Recently updated'
            )

    language = translation.get_language()

    article_prefix_translation = None
    if requires_article_prefix and language in ['ar'] and not tool_type_name:
        article_prefix_translation = pgettext(
            u'Tool list title article',
            # Translators: Used as a connected prefix to tool list titles which grammatically
            # require article prefixes before them, in certain languages such as Arabic.
            u'The'
        )

    format_args = {
        'featured': (featured_translation if is_featured else ''),
        'description': (description_translation or ''),
        'query': (query or ''),
        'tool_type': (tool_type_name or ''),
        'platform': (platform_locale_display_name or ''),
        'article_prefix': (article_prefix_translation or ''),
    }

    # =========================================
    # === Translate and format title string ===
    # =========================================

    if is_for_other_platforms:
        title = (
            pgettext(
                u'Tool list title',
                # Translators: Used for the “for other platforms” list that
                # appears in search views. The list includes all tools that
                # don’t have a version for the requested platform. Note that
                # the variables can be reordered as you see fit – the
                # tranlsation system is designed to allow different
                # ordering/formatting for different languages.
                u'{description} {featured} “{query}” {tool_type} {article_prefix}tools for other platforms'
            )
            .format(**format_args)
        )
    elif platform_locale_display_name and platform_locale_display_name != 'all':
        title = (
            pgettext(
                u'Tool list title',
                # Translators: Used for tool lists with an associated platform.
                # This string is provided separately from the non-platform-
                # specific string to give you more formatting flexibility. Note
                # that the variables can be reordered as you see fit – the
                # tranlsation system is designed to allow different
                # ordering/formatting for different languages.
                u'{description} {featured} “{query}” {tool_type} {article_prefix}tools for {platform}'
            )
            .format(**format_args)
        )
    else:
        title = (
            pgettext(
                u'Tool list title',
                # Translators: Used for tool lists without an associated
                # platform (i.e. if the global platform is “All tools”). This
                # string is provided separately from the non-platform-specific
                # string to give you more formatting flexibility. Note that the
                # variables can be reordered as you see fit – the tranlsation
                # system is designed to allow different ordering/formatting for
                # different languages.
                u'{description} {featured} “{query}” {tool_type} {article_prefix}tools'
            )
            .format(**format_args)
        )

    # =============================
    # === Clean up title string ===
    # =============================

    # Remove quotation marks if query ended up being blank
    title = re.sub(r'(“”|”“|\"\"|‘’|’‘|\'\')', u'', title)

    # Remove leading or trailing spaces
    title = re.sub(r'(^\s+|\s+$)', u'', title)

    # Remove extra interior spaces
    title = re.sub(r'(\s{2,})', u' ', title)

    return title
