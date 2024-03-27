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

u"""webfrontend cache utility functions."""

from django.core.cache import cache
from webfrontend import __version__ as webfrontend_version


def cache_key_data_to_cache_key(cache_key_data):
    cache_key_data[u'app_name'] = u'webfrontend'
    cache_key_data[u'app_version'] = webfrontend_version

    cache_key = u''

    for key in sorted(cache_key_data):
        cache_key += u'{key}={value}&'.format(
            key=key,
            value=cache_key_data[key],
        )

    return cache_key


def delete_cached_responses_matching_patterns(*delete_pattern_dicts):
    """
    Delete all keys matching provided dict patterns.

    Args:
        delete_pattern_dicts (dict): Dictionaries describing keys to delete
            (app_name and app_version are added automatically)

    Returns:
        None
    """
    for delete_pattern_dict in delete_pattern_dicts:
        delete_keys_matching_pattern(delete_pattern_dict)


def delete_keys_matching_pattern(delete_pattern_dict):
    """
    Delete all keys matching a dict pattern.

    Args:
        delete_pattern_dict (dict): Dictionary describing keys to delete
            (app_name and app_version are added automatically)

    Returns:
        None
    """
    delete_pattern_dict = delete_pattern_dict.copy()
    delete_pattern_dict[u'cache_type'] = u'response'

    cache.delete_pattern(
        pattern_dict_to_pattern_glob(delete_pattern_dict)
    )


def pattern_dict_to_pattern_glob(pattern_dict):
    pattern_dict[u'app_name'] = u'webfrontend'
    pattern_dict[u'app_version'] = webfrontend_version

    pattern_glob = u'*'

    for key in sorted(pattern_dict):
        pattern_glob += u'{key}={value}&*'.format(
            key=key,
            value=pattern_dict[key]
        )

    return pattern_glob
