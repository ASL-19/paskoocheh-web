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

u"""webfrontend URI utilities."""

from django.urls import reverse
from tools.models import Version
from urllib.parse import urlencode
from webfrontend.utils.query import (
    get_preferred_platform_slug_name_order,
    get_preferred_platform_slug_name_ordering_case,
)


def get_prefixed_query_string_args(query_string_args):
    u"""
    Returns a dict of query string args (probably from request.GET or
    context['request'].GET) with all keys prefixed with “q_”, for
    use in pask_reverse.

    Args:
        query_string_args (dict)

    Returns:
        dict
    """

    prefixed_query_string_args = {}
    for arg_key in query_string_args:
        prefixed_query_string_args['q_' + arg_key] = query_string_args[arg_key]

    return prefixed_query_string_args


def get_tool_preferred_version_path(tool, request):
    u"""
    Get the path to the preferred version of the provided tool.

    Args:
        request (WSGIRequest)

    Returns:
        URL path (unicode)
    """

    preferred_platform_slug_name = None

    if (
        hasattr(request, 'global_platform_slug') and
        request.global_platform_slug != 'all'
    ):
        preferred_platform_slug_name = request.global_platform_slug

    preferred_platform_slug_name_order = (
        get_preferred_platform_slug_name_order(request, preferred_platform_slug_name)
    )

    preferred_platform_slug_name_ordering_case = (
        get_preferred_platform_slug_name_ordering_case(
            preferred_platform_slug_name_order
        )
    )

    version = (
        Version.objects
        .filter(
            publishable=True,
            tool=tool,
        )
        .order_by(preferred_platform_slug_name_ordering_case)
        .first()
    )

    if version is not None:
        return pask_reverse(
            'webfrontend:toolversion',
            request,
            p_tool_id=tool.id,
            p_platform_slug=version.supported_os.slug_name,
        )
    else:
        return None


def pask_reverse(viewname, request, **kwargs):
    u"""
    Augmented replacement for Django’s django.urls.reverse that renders URLs
    with both path arguments (i.e. Django URL named group arguments) and query
    string arguments (which Django’s URL helpers don’t handle). Also includes
    “nocookies” query string argument when included in request.

    Path arguments should be prefixed with `p_`; query string arguments should
    be prefixed with `q_`.

    The arguments are prefixed and mixed rather than separated into
    dictionaries because this function is also wrapped as path_url template tag
    and template tags can’t take dict arguments. It would probably be confusing
    if pask_reverse and pask_url took different kwargs.

    e.g.:

    pask_reverse('webfrontend:toolversion', request,
        p_tool_id=1
        p_platform_slug='android'
        q_foo='bar'
    )
    https://paskoocheh.com/tools/1/android?foo=bar

    Arguments:
        viewname (str): Django URL pattern name
        request (WSGIRequest)
        **kwargs: Mixed path and query string arguments

    Returns:
        path_and_query_string (str) (absolute path and query string, doesn’t
            include hostname)
    """
    path_args = {}
    query_string_args = {}

    for key in kwargs:
        if key.startswith('p_'):
            path_args[key.replace('p_', '')] = kwargs[key]
            continue
        elif key.startswith('q_'):
            query_string_args[key.replace('q_', '')] = kwargs[key]
            continue

    path_and_query_string = reverse(viewname, kwargs=path_args)

    if len(query_string_args) > 0:
        if 'nocookies' in request.GET:
            path_and_query_string += (
                '?' + urlencode(query_string_args) + '&nocookies'
            )
        else:
            path_and_query_string += ('?' + urlencode(query_string_args))
    elif 'nocookies' in request.GET:
        path_and_query_string += '?nocookies'

    return path_and_query_string
