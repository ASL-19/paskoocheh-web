# -*- coding: utf-8 -*-
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

from django.db.models import Case, When

from tools.models import Tool
from stats.models import VersionDownload, VersionRating


def get_ordered_tools_by_platform(
        platform_slug,
        version_order_field):
    """
        Return all tools ordered for a specific platform

        Args,
        platform_slug(str): the platform to order tools on
        version_order_field(str = "(-?)download_count" | "(-?)star_rating"): a
            field that belongs to a model inheriting from VersionInstance
        Returns:
        A list of the ordered tools
    """

    if version_order_field in ['download_count', '-download_count']:
        model = VersionDownload

    if version_order_field in ['star_rating', '-star_rating']:
        model = VersionRating

    pk_list = list(
        model.objects.filter(
            platform_name=platform_slug)
        .order_by(version_order_field)
        .values_list('tool_id', flat=True)
        .distinct()
    )
    preserved = Case(
        *[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)]
    )

    return Tool.objects.filter(
        publishable=True,
        pk__in=pk_list)\
        .prefetch_related()\
        .order_by(preserved)


def prepare_queryset_filters(pk=None, slug=None, **filters):
    """
        Return filters to be used to get queryset of model by tool pk or slug

        Args:
        - pk: Tool pk
        - slug: Tool slug
        - **filters: Rest of the filter parameters
        Returns:
        - None if both pk and slug are provided
        - filters if either pk or slug were provided
    """

    if pk and slug:
        return None
    elif pk:
        filters['tool__pk'] = pk
    elif slug:
        filters['tool__slug'] = slug
    else:
        # Both pk and slug are None
        return None

    return filters


def get_object_by_tool_pk_or_slug(model, pk=None, slug=None, **filters):
    """
        Return filtered queryset of model by tool pk or slug

        Args:
        - model: VersionReview, VersionInstance...
        - pk: Tool pk
        - slug: Tool slug
        - **filters: Rest of the filter parameters
        Returns:
        - None if both pk and slug are provided
        - A model object if either pk or slug were provided
    """

    filters = prepare_queryset_filters(pk, slug, **filters)
    if not filters:
        return None
    return model.objects.get(**filters)


def filter_objects_by_tool_pk_or_slug(model, pk=None, slug=None, **filters):
    """
        Return filtered queryset of model by tool pk or slug

        Args:
        - model: VersionReview, VersionInstance...
        - pk: Tool pk
        - slug: Tool slug
        - **filters: Rest of the filter parameters
        Returns:
        - None if both pk and slug are provided
        - A django queryset if either pk or slug were provided
    """

    filters = prepare_queryset_filters(pk, slug, **filters)
    if not filters:
        return None
    return model.objects.filter(**filters)
