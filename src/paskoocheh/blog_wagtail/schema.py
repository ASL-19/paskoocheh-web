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

from wagtail.models import Page, Locale

from paskoocheh.utils import Connection

from static_page.types.captioned_image import (
    CaptionedImageBlock, CaptionedImageNode)
from static_page.types.document import DocumentBlock
from static_page.schema_helper import (
    CollapsibleBlock, TextBlock, MarkdownBlock)

from blog_wagtail.models import BlogIndexPage, PostPage, Topic


@strawberry.django.filters.filter(Topic, lookups=True)
class TopicFilter:
    name: strawberry.auto
    slug: strawberry.auto


@strawberry_django.type(Topic, pagination=True, filters=TopicFilter)
class TopicNode(strawberry.relay.Node):
    """
    Relay: Issue Node
    """

    id: strawberry.relay.NodeID[int]
    pk: int
    name: str
    slug: str


@strawberry.django.filters.filter(PostPage, lookups=True)
class BlogFilter:
    title: strawberry.auto
    published: strawberry.auto
    slug: strawberry.auto


@strawberry_django.type(PostPage, pagination=True, filters=BlogFilter)
class PostNode(strawberry.relay.Node):
    """
    Relay: Blog Post Page Node
    """

    id: strawberry.relay.NodeID[int]
    title: str
    slug: str
    numchild: int
    url_path: str
    seo_title: str
    search_description: str
    published: datetime.date
    featured_image: CaptionedImageNode
    read_time: Optional[float]
    synopsis: Optional[str]
    summary: Optional[str]

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        return queryset.live()

    @strawberry.field
    def topics(self) -> Optional[List[TopicNode]]:
        return self.topics.all()

    @strawberry.field
    def body(self) -> Optional[  # noqa C901
        List[
            strawberry.union(
                'PostBody',
                (
                    TextBlock,
                    MarkdownBlock,
                    CaptionedImageBlock,
                    DocumentBlock,
                    CollapsibleBlock
                )
            )
        ]
    ]:
        """
        Return repr based on block type
        """

        def repr_page(value):
            cls = Page.objects.get(pk=value).specific_class
            if cls == PostPage:
                return PostBlock(value=value)

            return None

        def repr_others(block_type, value):
            if block_type == 'text':
                return TextBlock(id=id, value=value)
            elif block_type == 'markdown':
                return MarkdownBlock(id=id, value=value)
            elif block_type == 'image':
                return CaptionedImageBlock(id=id, value=value)
            elif block_type == 'document':
                return DocumentBlock(id=id, value=value)
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
class PostBlock:
    """
    PostPage block for StreamField
    """

    @strawberry.field
    def post(self) -> Optional[PostNode]:
        return PostPage.objects.get(id=self.value, live=True)


@strawberry_django.type(BlogIndexPage, pagination=True)
class BlogIndexNode(strawberry.relay.Node):
    """
    Relay: Blog index page node
    """

    id: strawberry.relay.NodeID[int]
    title: str
    slug: str
    numchild: int
    url_path: str
    seo_title: str
    search_description: str
    image: CaptionedImageNode
    description: str

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        return queryset.live()


@strawberry.type
class BlogQuery:
    """
    Blog Query definition
    """

    @strawberry.field
    def blog_indices(
        self,
        info: strawberry.types.Info,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Optional[Connection[BlogIndexNode]]:
        blog_indices = BlogIndexPage.objects.all()
        return Connection[BlogIndexNode].resolve_connection(
            info=info,
            nodes=blog_indices,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def topic(self, locale: str, slug: str) -> Optional[TopicNode]:
        topic = None
        try:
            topic = Topic.objects.get(
                locale=Locale.objects.get(language_code=locale),
                slug=slug)
        except Topic.DoesNotExist:
            pass
        return topic

    @strawberry.field
    def topics(
        self,
        info: strawberry.types.Info,
        locale: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[TopicNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        topics = Topic.objects.filter(
            locale=Locale.objects.get(language_code=locale)).order_by(*order)
        return Connection[TopicNode].resolve_connection(
            info=info,
            nodes=topics,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def post(self, locale: str, slug: str) -> Optional[PostNode]:
        post = None
        try:
            post = PostPage.objects.get(
                locale=Locale.objects.get(language_code=locale),
                slug__iexact=slug,
                live=True)
        except PostPage.DoesNotExist:
            pass

        return post

    @strawberry.field
    def posts(
        self,
        info: strawberry.types.Info,
        locale: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
        topics: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[PostNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        topics = [] if topics is strawberry.UNSET else topics
        posts = PostPage.objects.filter(
            locale=Locale.objects.get(language_code=locale)).order_by(*order)
        if topics:
            topics_pks = Topic.objects.filter(
                slug__in=topics).values_list('pk')
            posts = posts.filter(topics__in=topics_pks).distinct()
        return Connection[PostNode].resolve_connection(
            info=info,
            nodes=posts,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def blog_index(self, locale: str) -> Optional[BlogIndexNode]:
        blog_index = None
        try:
            blog_index = BlogIndexPage.objects.get(
                locale=Locale.objects.get(language_code=locale),
                live=True)
        except BlogIndexPage.DoesNotExist:
            pass
        return blog_index
