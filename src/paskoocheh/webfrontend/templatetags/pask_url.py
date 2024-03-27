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

u"""Registers pask_url Django template tag."""

from django import template
from webfrontend.utils.uri import pask_reverse
register = template.Library()


@register.simple_tag(takes_context=True)
def pask_url(context, viewname, **kwargs):
    u"""
    Wrapper for webfrontend.utils.uri.pask_reverse.

    Arguments:
        context (RequestContext) (injected by decorator)
        viewname (str): Django URL pattern name
        **kwargs: Mixed path and query string arguments (see pask_reverse)

    Returns:
        Path and query string (str)
    """
    return pask_reverse(
        viewname,
        context.request,
        **kwargs
    )
