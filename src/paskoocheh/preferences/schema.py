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

import strawberry
import strawberry_django
from typing import Optional, List

from paskoocheh.utils import Connection

from preferences.models import (
    ToolType,
    Platform)


@strawberry_django.type(ToolType, pagination=True)
class ToolTypeNode(strawberry.relay.Node):
    """
    Relay: Tool Type node
    """
    id: strawberry.relay.NodeID[int]
    pk: int
    name: str
    name_fa: Optional[str]
    name_ar: Optional[str]
    slug: str
    icon: Optional[str]


@strawberry_django.type(Platform, pagination=True)
class PlatformNode(strawberry.relay.Node):
    """
    Relay: Tool Type node
    """
    id: strawberry.relay.NodeID[int]
    pk: int
    name: str
    display_name: str
    display_name_fa: Optional[str]
    display_name_ar: Optional[str]
    slug_name: str
    category: strawberry.auto
    icon: Optional[str]


@strawberry.type
class PreferencesQuery:

    @strawberry.field
    def tool_type(self, slug: str) -> Optional[ToolTypeNode]:
        try:
            tool_type = ToolType.objects.get(
                slug=slug)
        except ToolType.DoesNotExist:
            return None
        return tool_type

    @strawberry.field
    def platform(self, slug: str) -> Optional[PlatformNode]:
        try:
            platform = Platform.objects.get(
                slug_name=slug)
        except Platform.DoesNotExist:
            return None
        return platform

    @strawberry.field
    def tool_types(
        self,
        info: strawberry.types.Info,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET
    ) -> Optional[Connection[ToolTypeNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        tool_types = ToolType.objects.all().order_by(*order)
        return Connection[ToolTypeNode].resolve_connection(
            info=info,
            nodes=tool_types,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def platforms(
        self,
        info: strawberry.types.Info,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET
    ) -> Optional[Connection[PlatformNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        platforms = Platform.objects.all().order_by(*order)
        return Connection[PlatformNode].resolve_connection(
            info=info,
            nodes=platforms,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)
