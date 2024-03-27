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

import uuid
import datetime

import strawberry
import strawberry_django
from strawberry_django.pagination import OffsetPaginationInput
from typing import Optional, Iterable

from paskoocheh.utils import Connection

from wagtail.embeds.models import Embed


@strawberry.django.filters.filter(Embed, lookups=True)
class EmbedFilter:
    provider_name: strawberry.auto


@strawberry_django.type(Embed, pagination=True, filters=EmbedFilter)
class EmbedNode(strawberry.relay.Node):
    """
    Embed Node
    """

    id: strawberry.relay.NodeID[int]
    cache_until: Optional[datetime.datetime]
    hash: Optional[str]
    height: Optional[int]
    html: Optional[str]
    last_updated: Optional[datetime.datetime]
    max_width: Optional[int]
    provider_name: Optional[str]
    thumbnail_url: Optional[str]
    title: Optional[str]
    type: Optional[str]
    url: Optional[str]
    width: Optional[int]


@strawberry.type
class EmbedBlock:
    """
    Embed block for StreamField
    """

    id: uuid.UUID

    @strawberry.field
    def embed(self) -> Optional[EmbedNode]:
        return Embed.objects.get(url=self.value)


@strawberry.type
class EmbedQuery:
    """
    Embed Queries
    """

    @strawberry.field
    def embed(self, pk: int) -> Optional[EmbedNode]:
        return Embed.objects.get(pk=pk)

    @strawberry_django.connection(Connection[EmbedNode])
    def embeds(
        self,
        pagination: Optional[OffsetPaginationInput] = strawberry.UNSET
    ) -> Iterable[EmbedNode]:
        embeds = Embed.objects.all()
        return strawberry_django.pagination.apply(pagination, embeds)
