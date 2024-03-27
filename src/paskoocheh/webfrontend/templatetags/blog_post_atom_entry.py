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

u"""Registers blog_post_atom_entry template tag."""

from django import template
from markdownx.utils import markdownify
from webfrontend.utils.blog import get_localized_blog_category_name
from webfrontend.utils.general import enforce_required_args
from webfrontend.utils.uri import pask_reverse

register = template.Library()


@register.inclusion_tag(
    'webfrontend/tags/blog_post_atom_entry.xml',
    takes_context=True,
)
def blog_post_atom_entry(
    context,
    post=None,
):
    u"""
    Build the context for the blog_post_list inclusion tag.

    Args:
        Required:
            heading_tag (str): Heading tag for post titles (e.g. 'h3')
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
    post_updated_datetime_iso8601 = (
        post.last_modified_date
        .replace(microsecond=0)
        .isoformat()
    )

    post_url = context.request.build_absolute_uri(
        pask_reverse(
            'webfrontend:blogpost',
            context.request,
            p_post_date=post_published_date_iso8601,
            p_post_slug=post.slug,
        )
    )

    post_category_name = get_localized_blog_category_name(
        post.category,
        context.request,
    )

    post_content_html = markdownify(post.content)

    return {
        'post': post,
        'post_category_name': post_category_name,
        'post_content_html': post_content_html,
        'post_url': post_url,
        'post_published_datetime_iso8601': post_published_datetime_iso8601,
        'post_updated_datetime_iso8601': post_updated_datetime_iso8601,
    }
