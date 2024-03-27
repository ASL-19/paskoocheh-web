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

u"""Registers blog_post_list template tag."""

from django import template
from webfrontend.utils.general import enforce_required_args
from django.conf import settings

register = template.Library()


@register.inclusion_tag('webfrontend/tags/blog_post_list.html')
def blog_post_list(
    displayed_rows_limit=None,
    post_heading_tag=None,
    posts=None,
    show_summary=None,
    disable_jalali=None,
    current_view_name=None
):
    u"""
    Build the context for the blog_post_list inclusion tag.

    Args:
        posts (List of blog.models.Post)

    Args:
        Required:
            post_heading_tag (str): Heading tag for post titles (e.g. 'h3')
            posts (List of blog.models.Post)
        Optional
            displayed_rows_limit (int): Number of rows to be displayed, Only 2
                or 3 supported, though easy to extend. All provided posts will
                be rendered in HTML, but display will be limited via CSS. Number
                of displayed items is dependant on viewport width.
            show_summary (boolean): A switch for showing/hiding summaries. The
                default is false; summaries won't show by default. When activated,
                dates would hide automatically
            disable_jalali (boolean): A switch for enabling/disabling Jalali
                calendar dates. When this property is activated, Gregorian
                dates should show up instead. This was added for Zanga.

    Returns:
        dictionary: Template context
    """
    enforce_required_args(locals(), 'post_heading_tag', 'posts')

    disable_jalali = True if settings.PLATFORM == 'zanga' else False

    return {
        'post_heading_tag': post_heading_tag,
        'posts': posts,
        'displayed_rows_limit': displayed_rows_limit,
        'show_summary': show_summary,
        'disable_jalali': disable_jalali,
        'current_view_name': current_view_name
    }
