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

u"""webfrontend tool utilities."""

import logging

from django.db.models import Case, Prefetch, Q, When
from tools.models import Info, Image, Version

logger = logging.getLogger(__name__)


def add_prefetch_related_to_tools_queryset(tools_queryset, request, preferred_platform_slug_name=None):
    u"""
    Returns the given QuerySet with publishable versions and logo images
    preloaded. Versions are preferentially ordered based on the request’s user
    agent and preferred_platform_slug_name.

    Args:
        tools_queryset (QuerySet): QuerySet for tools, probably from index or
            search controllers
        request (WSGIRequest)

    Returns:
        tools_queryset_with_prefetches (QuerySet)
    """
    preferred_platform_slug_name_order = (
        get_preferred_platform_slug_name_order(request, preferred_platform_slug_name)
    )

    preferred_platform_slug_name_ordering_case = (
        get_preferred_platform_slug_name_ordering_case(
            preferred_platform_slug_name_order
        )
    )

    versions_queryset = (
        Version.objects
        .filter(
            publishable=True,
        )
        .order_by(
            preferred_platform_slug_name_ordering_case
        )
    )

    tools_queryset_with_prefetches = (
        tools_queryset.prefetch_related(
            Prefetch(
                'versions',
                queryset=versions_queryset,
            )
        )
        # TODO: It would be slightly more efficient if this only fetched the
        # necessary platforms instead of always getting them all, but it
        # doesn’t seem to be easy to do. It’s already a fast query, so not a
        # big deal.
        .prefetch_related(
            Prefetch(
                'versions__supported_os',
            )
        ).prefetch_related(
            Prefetch(
                'images',
                queryset=(
                    Image.objects
                    .filter(
                        Q(image_type='logo') &
                        (
                            Q(language__isnull=True) |
                            Q(language=request.LANGUAGE_CODE)
                        ) &
                        Q(publish=True)
                    )
                    .order_by('order')
                ),
                to_attr='logo_images',
            )
        ).prefetch_related(
            Prefetch(
                'infos',
                queryset=Info.objects.filter(
                    language=request.LANGUAGE_CODE,
                    publishable=True,
                ),
                to_attr='infos_current_language',
            )
        )
    )

    return tools_queryset_with_prefetches


def add_select_related_to_faqs_queryset(faqs_queryset):
    u"""
    Returns the given QuerySet with tool, version, and version.supported_os
    (Platform) selected

    Args:
        faqs_queryset (QuerySet): QuerySet for tools.models.Faq entities

    Returns:
        faqs_queryset_with_related_selected (QuerySet)
    """
    faqs_queryset_with_related_selected = (
        faqs_queryset
        .select_related('tool', 'version', 'version__supported_os')
    )

    return faqs_queryset_with_related_selected


def add_select_related_to_tutorials_queryset(tutorials_queryset):
    u"""
    Returns the given QuerySet with version, and version.supported_os
    (Platform) selected

    Args:
        tutorials_queryset (QuerySet): QuerySet for tools.models.Tutorial
        entities

    Returns:
        tutorials_queryset_with_related_selected (QuerySet)
    """
    tutorials_queryset_with_related_selected = (
        tutorials_queryset
        .select_related('version', 'version__supported_os')
    )

    return tutorials_queryset_with_related_selected


def get_filter_platform_slugs(primary_platform_slug):
    u"""
    Returns an array of platform slugs to be used in tool query. If the
    primary platform slug is a desktop OS, Chrome and Firefox are appended;
    otherwise, it just contains the primary platform slug.

    Args:
        primary_platform_slug (str): Platform slug of the query

    Returns:
        filter_platform_slugs (array): Array containing all platform slugs to be
        queried (probably used as the value of a
        versions__supported_os__slug_name__in kwarg)
    """
    filter_platform_slugs = [primary_platform_slug]

    if primary_platform_slug in ['linux', 'macos', 'windows']:
        filter_platform_slugs.extend(['chrome', 'firefox'])

    return filter_platform_slugs


def get_preferred_platform_slug_name_order(request, preferred_platform_slug_name=None):
    u"""
    Get a list of Platform.slug_name values in order of preference, based on
    several factors.

    Starts with a default hard-coded preferred order of slug_name values (based
    on popularity). If preferred_platform_slug_name is provided, it’s pushed to the
    top of the list; otherwise, a preferred Platform.supported_os value is chosen based on the
    request’s user agent.

    Args:
        request (WSGIRequest)

    Returns:
        preferred_platform_slug_name_order (list)
    """

    from webfrontend.utils.general import get_ua_default_platform_slug_name_os

    # Initial order is based on the platform download popularity. Chrome and
    # Firefox pushed to top if preferred platform is desktop.
    if preferred_platform_slug_name in ['linux', 'macos', 'windows']:
        preferred_platform_slug_name_order = [
            'chrome',
            'firefox',
            'android',
            'windows',
            'ios',
            'macos',
            'linux',
            'windowsphone',
            'linux32',
            'windows32',
        ]
    else:
        preferred_platform_slug_name_order = [
            'android',
            'windows',
            'ios',
            'chrome',
            'firefox',
            'macos',
            'linux',
            'windowsphone',
            'linux32',
            'windows32',
        ]

    if preferred_platform_slug_name is None:
        preferred_platform_slug_name = get_ua_default_platform_slug_name_os(request)

    if not preferred_platform_slug_name:
        return preferred_platform_slug_name_order

    try:
        preferred_platform_slug_name_order.insert(
            0,
            preferred_platform_slug_name_order.pop(
                preferred_platform_slug_name_order.index(
                    preferred_platform_slug_name
                )
            )
        )
    except ValueError:
        logger.warning(
            u'Something went wrong while attempting to reorder preferred_platform_slug_name_order.'
        )

    return preferred_platform_slug_name_order


def get_preferred_platform_slug_name_ordering_case(preferred_platform_slug_name_order):
    u"""
    Returns a Case that can be used to order Version instances by
    preferred_platform_slug_name_order.

    GH: I don’t know SQL well enough to fully understand how this works, but it
    has the effect of ordering the versions by the
    preferred_platform_slug_name_order. I assume doing this via SQL is more
    efficient than sorting the data in Python.

    Via https://stackoverflow.com/a/38390480/7949868
    """
    return Case(
        *[
            When(supported_os__slug_name=order_supported_os, then=order_index)
            for order_index, order_supported_os
            in enumerate(preferred_platform_slug_name_order)
        ]
    )
