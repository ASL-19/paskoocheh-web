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

u"""Registers blog_post_list_item template tag."""

from django import template
from webfrontend.utils.blog import get_localized_blog_category_name
from webfrontend.utils.general import (
    enforce_required_args,
    gregorian_datetime_to_jalali_date_string,
    image_exists,
)
from webfrontend.utils.uri import pask_reverse
from django.conf import settings

register = template.Library()


@register.inclusion_tag(
    'webfrontend/tags/blog_post_list_item.html',
    takes_context=True,
)
def blog_post_list_item(
    context,
    heading_tag=None,
    post=None,
    show_summary=None,
    disable_jalali=None,
    current_view_name=None
):
    u"""
    Build the context for the blog_post_list inclusion tag.

    Args:
        Required:
            heading_tag (str): Heading tag for post titles (e.g. 'h3')
            post (blog.models.Post)
        Optional:
            show_summary (boolean): A switch for showing/hiding summaries. The
                default is false; summaries won't show by default. When activated,
                dates would hide automatically
            disable_jalali (boolean): A switch for enabling/disabling Jalali
                calendar dates. When this property is activated, Gregorian
                dates should show up instead. This was added for Zanga.

    Returns:
        dictionary: Template context
    """
    enforce_required_args(locals(), 'heading_tag', 'post')

    post_published_date_jalali = gregorian_datetime_to_jalali_date_string(
        post.published_date
    )
    post_published_datetime_iso8601 = (
        post.published_date
        .replace(microsecond=0)
        .isoformat()
    )
    post_published_date_iso8601 = post_published_datetime_iso8601[:10]

    image = None
    # If the image’s aspect ratio is a close fit for the 2.5:1 container
    # (>2.4:1 and <2.6:1) it’s stretched to fit the container to avoid awkward
    # rendering / margins.
    image_aspect_ratio_is_wider_than_container = False

    if image_exists(post.feature_image):
        image = post.feature_image

        image_aspect_ratio = (
            float(image.width) / float(image.height)
        )

        if image_aspect_ratio > 2.5:
            image_aspect_ratio_is_wider_than_container = True

    post_category_name = get_localized_blog_category_name(
        post.category,
        context.request,
    )

    post_path = pask_reverse(
        'webfrontend:blogpost',
        context.request,
        p_post_date=post_published_date_iso8601,
        p_post_slug=post.slug,
    )

    default_image_path = settings.WEBFRONTEND_DEFAULT_IMAGE_PATH

    return {
        'heading_tag': heading_tag,
        'image': image,
        'image_aspect_ratio_is_wider_than_container': (
            image_aspect_ratio_is_wider_than_container
        ),
        'post': post,
        'post_category_name': post_category_name,
        'post_path': post_path,
        'post_published_date_jalali': post_published_date_jalali,
        'post_published_datetime_iso8601': post_published_datetime_iso8601,
        'default_image_path': default_image_path,
        'show_summary': show_summary,
        'disable_jalali': disable_jalali,
        'current_view_name': current_view_name,
    }
