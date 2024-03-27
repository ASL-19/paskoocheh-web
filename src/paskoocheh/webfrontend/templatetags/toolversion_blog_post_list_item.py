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

u"""Registers toolversion_blog_post_list_item Django template tag."""

from django import template
from webfrontend.utils.general import (
    enforce_required_args,
    gregorian_datetime_to_jalali_date_string,
)
from django.conf import settings

app = settings.PLATFORM

register = template.Library()


@register.inclusion_tag(
    'webfrontend/tags/toolversion_blog_post_list_item.html',
    takes_context=True,
)
def toolversion_blog_post_list_item(
    context,
    post=None,
):
    u"""
    Build the context for the toolversion_blog_post_list_item inclusion tag.

    Args:
        Required:
            post (blog.models.Post)

    Returns:
        dictionary: Template context
    """
    enforce_required_args(locals(), 'post')

    post_published_datetime_iso8601 = (
        post.published_date
        .replace(microsecond=0)
        .isoformat()
    )
    post_published_date_iso8601 = post_published_datetime_iso8601[:10]
    post_published_date_jalali = gregorian_datetime_to_jalali_date_string(
        post.published_date
    )

    return {
        'post': post,
        'post_published_date_iso8601': post_published_date_iso8601,
        'post_published_date_jalali': post_published_date_jalali,
        'post_published_datetime_iso8601': post_published_datetime_iso8601,
        'app': app,
    }
