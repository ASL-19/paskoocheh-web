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

u"""webfrontend responses cache decorator."""

from django.conf import settings
from django.utils.decorators import method_decorator
from fancy_cache import cache_page
from webfrontend.caches.utils import cache_key_data_to_cache_key
from webfrontend.utils.general import is_request_user_agent_noop


# =======================
# === Cache decorator ===
# =======================
def get_cache_key_prefix(request):
    # Data included in every key
    cache_key_data = {
        u'cache_type': u'response',
        u'global_platform_slug': request.global_platform_slug,
        u'is_noop': str(is_request_user_agent_noop(request)).lower(),
        u'url_name': request.resolver_match.url_name,
    }

    # Add path arguments (urls.py named groups)
    for key in request.resolver_match.kwargs:
        if key != u'path_prefix':
            cache_key_data_key = u'p_{key}'.format(key=key)
            cache_key_data[cache_key_data_key] = request.resolver_match.kwargs[key]

    # Add query (GET) arguments
    for key in request.GET:
        cache_key_data_key = u'q_{key}'.format(key=key)
        cache_key_data[cache_key_data_key] = request.GET[key]

    # Compile cache key
    cache_key_prefix = cache_key_data_to_cache_key(cache_key_data)

    return cache_key_prefix


def pk_cache_response(timeout=settings.WEBFRONTEND_CACHE_RESPONSE_TIMEOUT):
    if settings.WEBFRONTEND_CACHE_RESPONSE_ENABLED:
        return method_decorator(
            cache_page(
                timeout,
                key_prefix=get_cache_key_prefix,
            )
        )
    else:
        return lambda function: function
