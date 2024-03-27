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

u"""Registers toolversion_blog_post_list Django template tag."""

from django import template
from webfrontend.utils.general import enforce_required_args

register = template.Library()


@register.inclusion_tag(
    'webfrontend/tags/toolversion_blog_post_list.html',
)
def toolversion_blog_post_list(
    posts=None,
):
    u"""
    Build the context for the toolversion_blog_post_list inclusion tag.

    Args:
        Required:
            posts (iterable of blog.models.Post)

    Returns:
        dictionary: Template context
    """
    enforce_required_args(locals(), 'posts')

    return {
        'posts': posts,
    }
