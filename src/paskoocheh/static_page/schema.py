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

import datetime

import strawberry
import strawberry_django
from typing import List, Optional

from paskoocheh.utils import Connection

from wagtail.models import Page, Locale

from static_page.models import StaticPage
from static_page.types.generic import GenericBlock
from static_page.types.captioned_image import (
    CaptionedImageBlock, CaptionedImageNode)
from static_page.types.document import DocumentBlock

from static_page.schema_helper import TextBlock, CollapsibleBlock


@strawberry.type
class LinkBlock(GenericBlock):
    pass


@strawberry.type
class EmailBlock(GenericBlock):
    pass


@strawberry.django.filters.filter(StaticPage, lookups=True)
class StaticPageFilter:
    title: strawberry.auto
    published: strawberry.auto
    slug: strawberry.auto


@strawberry_django.type(StaticPage, pagination=True, filters=StaticPageFilter)
class StaticPageNode(strawberry.relay.Node):
    """
    Relay: Static Page Node
    """

    id: strawberry.relay.NodeID[int]
    title: str
    slug: str
    numchild: int
    url_path: str
    seo_title: str
    search_description: str
    published: datetime.date
    image: Optional[CaptionedImageNode]

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        return queryset.live()

    @strawberry.field
    def body(self) -> Optional[  # noqa C901
        List[
            strawberry.union(
                'StaticPageBody',
                (
                    TextBlock,
                    CaptionedImageBlock,
                    DocumentBlock,
                    LinkBlock,
                    EmailBlock,
                    CollapsibleBlock,
                )
            )
        ]
    ]:
        """
        Return repr based on block type
        """

        def repr_page(value):
            cls = Page.objects.get(pk=value).specific_class
            if cls == StaticPage:
                return StaticPageBlock(value=value)

            return None

        def repr_others(block_type, value):
            if block_type == 'text':
                return TextBlock(id=id, value=value)
            elif block_type == 'image':
                return CaptionedImageBlock(id=id, value=value)
            elif block_type == 'document':
                return DocumentBlock(id=id, value=value)
            elif block_type == 'link':
                return LinkBlock(id=id, value=value)
            elif block_type == 'email':
                return EmailBlock(id=id, value=value)
            elif block_type == 'collapsible':
                return CollapsibleBlock(id=id, value=value)

            return None

        repr_body = []
        for block in self.body.raw_data:

            block_type = block.get('type')
            id = block.get('id')
            value = block.get('value')

            if block_type == 'page':
                block = repr_page(value)
                if block is not None:
                    repr_body.append(block)
            else:
                block = repr_others(block_type, value)
                if block is not None:
                    repr_body.append(block)

        return repr_body


@strawberry.type
class StaticPageBlock:
    """
    StaticPage block for StreamField
    """

    @strawberry.field
    def page(self) -> Optional[StaticPageNode]:
        return StaticPage.objects.get(id=self.value, live=True)


@strawberry.type
class StaticPageQuery:
    """
    Static page Query definition
    """

    @strawberry.field
    def static_page(self, locale: str, slug: str) -> Optional[StaticPageNode]:
        static_page = None
        try:
            static_page = StaticPage.objects.get(
                locale=Locale.objects.get(language_code=locale),
                slug__iexact=slug,
                live=True)
        except StaticPage.DoesNotExist:
            pass

        return static_page

    @strawberry.field
    def static_pages(
        self,
        info: strawberry.types.Info,
        locale: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[StaticPageNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        static_pages = StaticPage.objects.filter(
            locale=Locale.objects.get(language_code=locale)).order_by(*order)
        return Connection[StaticPageNode].resolve_connection(
            info=info,
            nodes=static_pages,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)
