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

u"""webfrontend blog utilities."""

import re

from django.utils.translation import pgettext


def get_blog_post_list_title(**kwargs):
    u"""
    Returns a translated tool list title based on the provided kwargs.

    Args:
        Optional:
            category_name (unicode)
            is_featured (bool)
                True if list is limited to featured tools. False is unsupported.
            platform_locale_display_name (unicode)
            tool_name (unicode)

    Returns:
        Unicode string
    """
    category_name = kwargs.get('category_name', None)
    is_featured = kwargs.get('is_featured', False)
    platform_locale_display_name = kwargs.get('platform_locale_display_name', None)
    tool_name = kwargs.get('tool_name', None)

    if platform_locale_display_name and not tool_name:
        raise TypeError('If platform_locale_display_name is provided, tool_name must be set')

    title = None

    featured_translation = pgettext(
        u'List title',
        u'Featured',
    )

    if tool_name and platform_locale_display_name:
        title = (
            pgettext(
                u'Blog post list title',
                # Translators: Used for blog post list titles (e.g. on the blog
                # homepage, category pages, etc.). Note that the variables can
                # be reordered as you see fit – the tranlsation system is
                # designed to allow different ordering/formatting for different
                # languages.
                u'{featured} {category_name} blog posts about {tool_name} for {platform_name}'
            )
            .format(
                category_name=category_name or '',
                featured=(
                    featured_translation if is_featured else ''
                ),
                tool_name=tool_name,
                platform_name=platform_locale_display_name,
            )
        )
    elif tool_name:
        title = (
            pgettext(
                u'Blog post list title',
                # Translators: Used for blog post list titles (e.g. on the blog
                # homepage, category pages, etc.). Note that the variables can
                # be reordered as you see fit – the tranlsation system is
                # designed to allow different ordering/formatting for different
                # languages.
                u'{featured} {category_name} blog posts about {tool_name}'
            )
            .format(
                category_name=category_name or '',
                featured=(
                    featured_translation if is_featured else ''
                ),
                tool_name=tool_name,
            )
        )
    elif category_name and is_featured:
        title = (
            pgettext(
                u'Blog post list title',
                # Translators: Used for blog post list titles (e.g. on the blog
                # homepage, category pages, etc.). Note that the variables can
                # be reordered as you see fit – the tranlsation system is
                # designed to allow different ordering/formatting for different
                # languages.
                u'{featured} {category_name} blog posts'
            )
            .format(
                category_name=category_name,
                featured=featured_translation,
            )
        )
    elif category_name:
        title = (
            pgettext(
                u'Blog post list title',
                # Translators: Used for blog post list titles (e.g. on the blog
                # homepage, category pages, etc.). Note that the variables can
                # be reordered as you see fit – the tranlsation system is
                # designed to allow different ordering/formatting for different
                # languages.
                u'{category_name} blog posts'
            )
            .format(
                category_name=category_name,
            )
        )
    elif is_featured:
        title = (
            pgettext(
                u'Blog post list title',
                # Translators: Used for blog post list titles (e.g. on the blog
                # homepage, category pages, etc.). Note that the variables can
                # be reordered as you see fit – the tranlsation system is
                # designed to allow different ordering/formatting for different
                # languages.
                u'Featured blog posts'
            )
        )
    else:
        title = (
            pgettext(
                u'Blog post list title',
                # Translators: Used for blog post list titles (e.g. on the blog
                # homepage, category pages, etc.). Note that the variables can
                # be reordered as you see fit – the tranlsation system is
                # designed to allow different ordering/formatting for different
                # languages.
                u'Latest blog posts'
            )
        )

    # Remove leading or trailing spaces
    title = re.sub(r'(^\s+|\s+$)', u'', title)

    # Remove empty quotation marks
    title = re.sub(r'(”“)', u'', title)

    # Remove extra interior spaces
    title = re.sub(r'(\s{2,})', u' ', title)

    return title


def get_localized_blog_category_name(category, request):
    u"""
    Get the name of the provided blog category in the current language.

    Args:
        category (blog.models.Category)
        request (WSGIRequest)
    Returns:
        unicode
    """
    if not category:
        return None

    category_name = getattr(category, 'name', None)

    if request.LANGUAGE_CODE == 'ar' and category.name_ar:
        category_name = category.name_ar
    elif request.LANGUAGE_CODE == 'fa' and category.name_fa:
        category_name = category.name_fa

    return category_name
