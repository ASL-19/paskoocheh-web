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

u"""Webfrontend context processors (template tags)."""


def view_body_class(request):
    u"""
    Returns class for the <body> element based on the request’s
    url_name attribute.

    Args:
       request (HTTPRequest)

    Returns:
        dictionary: Template context
    """
    view_body_class = ''

    if (
        hasattr(request, 'resolver_match') and
        hasattr(request.resolver_match, 'url_name') and
        request.resolver_match.url_name is not None and
        len(request.resolver_match.url_name) > 0
    ):
        view_body_class = ('pk-' + request.resolver_match.url_name)

    return {
        'view_body_class': view_body_class
    }
