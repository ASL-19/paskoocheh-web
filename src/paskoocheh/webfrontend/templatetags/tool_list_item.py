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

import attr
import unicodedata
from django import template
from django.utils import translation

register = template.Library()

MAX_TOOL_NAME_LENGTH = 24


@attr.s(frozen=True, slots=True)
class ToolListItemContext(object):
    u"""
    Immutable object containing data for a tool list item. Passed to template
    as dictionary.

    Attributes:
        average_rating_display (str): Average rating, rounded down to one
            decimal point
        download_count (int)
        logo (Image)
        name (unicode)
        platform_slug (unicode)
        should_display_browser_badge (bool)
        version (Version)
        in_search_view (bool)
    """
    download_count = attr.ib()
    logo = attr.ib()
    name = attr.ib()
    name_inner_html = attr.ib(init=False)
    platform_slug = attr.ib()
    should_display_all_platform_stats = attr.ib()
    should_display_browser_badge = attr.ib()
    tool_type_localized_name = attr.ib(init=False)
    version = attr.ib()
    versiondownload_cache_placeholder = attr.ib(init=False)
    versionrating_cache_placeholder = attr.ib(init=False)
    in_search_view = attr.ib()

    def __attrs_post_init__(self):
        # ---------------------------
        # --- Set name_inner_html ---
        # ---------------------------
        name_inner_html = get_name_inner_html(self.name)

        object.__setattr__(
            self,
            'name_inner_html',
            name_inner_html
        )

        # ------------------------------------
        # --- Set tool_type_localized_name ---
        # ------------------------------------
        tool_type = self.version.tool.tooltype.first()
        tool_type_localized_name = None

        language = translation.get_language()

        if tool_type:
            if language == 'fa':
                tool_type_localized_name = getattr(tool_type, 'name_fa')
            elif language == 'ar':
                tool_type_localized_name = getattr(tool_type, 'name_ar')
            else:
                tool_type_localized_name = getattr(tool_type, 'name')

        object.__setattr__(
            self,
            'tool_type_localized_name',
            tool_type_localized_name
        )

        # -------------------------------------------------
        # --- Set versiondownload_cache_placeholder and ---
        # --- versionrating_cache_placeholder           ---
        # -------------------------------------------------
        if self.should_display_all_platform_stats:
            platform_slug_name = 'all'
        else:
            platform_slug_name = self.version.supported_os.slug_name

        object.__setattr__(
            self,
            'versiondownload_cache_placeholder',
            '[stat_versiondownload_{tool_id}_{platform_slug_name}]'.format(
                tool_id=self.version.tool.id,
                platform_slug_name=platform_slug_name,
            )
        )

        object.__setattr__(
            self,
            'versionrating_cache_placeholder',
            '[stat_versionrating_{tool_id}_{platform_slug_name}]'.format(
                tool_id=self.version.tool.id,
                platform_slug_name=platform_slug_name,
            )
        )


def get_name_inner_html(name):
    u"""
    Generate the inner HTML of a tool list item heading.

    If length of name is shorter than MAX_TOOL_NAME_LENGTH, full name is
    returned.

    If length of name is longer than MAX_TOOL_NAME_LENGTH, returned string
    consists of:
    - Truncated name (visible)
    - Ellipsis (visible, but hidden from screen readers, and hopefully hidden
      from search engines)
    - Remainder of name (invisible, but exposed to screen readers, and hopefully
      visible to search engines)

    The idea of this split is to avoid unnecessarily cutting off the tool name
    to screen readers, since a partial name could be confusing, and there’s no
    non-visual need to cut it off.

    It’s hard to know for sure how search engines or other crawlers will expose
    ARIA attributes or inline `display: none`, but ideally, they will ignore the
    ellipsis and therefore interpret and index the heading as, e.g. “Open VPN
    for Android” rather than “Open VPN for… Android”.
    """
    if (
        name.find(' ') == -1 or  # Name is one word
        len(name) <= MAX_TOOL_NAME_LENGTH  # Name is shorter than max length
    ):
        return name
    else:
        first_word = name.split(' ')[0]

        # Based on https://stackoverflow.com/a/250373/7949868
        if len(first_word) >= MAX_TOOL_NAME_LENGTH:
            truncated_name = first_word
        else:
            truncated_name = name[:MAX_TOOL_NAME_LENGTH].rsplit(' ', 1)[0]

        name_remainder = name.replace(truncated_name, '')

        name_inner_html = (
            u'<span class="visible">{truncated_name}</span>'.format(
                truncated_name=truncated_name
            )
        )

        # If the truncated name contains any character with RTL bidirectional
        # class, we style the ellipsis with `unicode-bidi: embed` in order to
        # get it to appear on the appropriate side. This way we don’t end up
        # with stuff like “…Open VPN for” rather than “Open VPN for…”
        #
        # See:
        # - https://stackoverflow.com/a/17685399/7949868
        # - https://developer.mozilla.org/en-US/docs/Web/CSS/unicode-bidi

        truncated_name_has_rtl_characters = False

        for character in truncated_name:
            if unicodedata.bidirectional(character) in ('AL', 'R'):
                truncated_name_has_rtl_characters = True
                break

        if truncated_name_has_rtl_characters:
            name_inner_html += u'''<span
                aria-hidden="true"
                class="ellipsis"
                role="presentation"
                style="display: none;"
            >…</span>'''
        else:
            name_inner_html += u'''<span
                aria-hidden="true"
                class="ellipsis ltr"
                role="presentation"
                style="display: none;"
            >…</span>'''

        name_inner_html += (
            u'<span class="pk-g-invisible">{name_remainder}</span>'.format(
                name_remainder=name_remainder
            )
        )

        return name_inner_html


@register.inclusion_tag('webfrontend/tags/tool_list_item.html')
def tool_list_item(tool_list_item_context):
    u"""
    Build the context for the tool_list_item inclusion tag.

    Args:
        tool_list_item_context (ToolListItemContext)

    Returns:
        dictionary: Template context
    """

    return {
        attribute: getattr(tool_list_item_context, attribute, None)
        for attribute in tool_list_item_context.__slots__
    }
