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

u"""Registers blog_associated_tool_list template tag."""

from django import template

register = template.Library()


@register.inclusion_tag('webfrontend/tags/blog_associated_tool_list.html')
def blog_associated_tool_list(
    associated_tools=None,
    associated_versions=None,
):
    u"""
    Build the context for the blog_associated_tool_list inclusion tag.

    Args:
        Optional:
            associated_tools (iterable of Tool)
            associated_versions (iterable of Version)

    Returns:
        dictionary: Template context
    """

    return {
        'associated_tools': associated_tools,
        'associated_versions': associated_versions,
    }
