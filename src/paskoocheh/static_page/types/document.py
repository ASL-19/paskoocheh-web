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
import mimetypes

import strawberry
import strawberry_django

from typing import Optional, Iterable, List

from wagtail.documents import get_document_model

from static_page.types.tag import FlatTags
from static_page.types.generic import GenericScalar
from paskoocheh.media_storage import get_s3_url
from paskoocheh.utils import Connection


Document = get_document_model()


@strawberry_django.type(Document, pagination=True)
class DocumentNode(strawberry.relay.Node):
    """
    Document Node
    """

    id: strawberry.relay.NodeID[int]
    file_size: Optional[int]
    url: Optional[str]
    file_type: Optional[str]
    content_type: Optional[str]
    file_hash: str
    title: str
    file: str
    created_at: datetime.datetime

    @strawberry.field
    def url(self) -> str:
        url = self.url
        s3_url = get_s3_url()
        if s3_url:
            url = url.replace(s3_url, '')

        return url

    @strawberry.field
    def file_type(self) -> str:
        return self.file.name.split('.')[-1].lower()

    @strawberry.field
    def content_type(self) -> str:
        return mimetypes.guess_type(self.file.name)[0]

    @strawberry.field
    def tags(self) -> Optional[List[Optional[FlatTags]]]:
        return self.tags.all().order_by('slug')


@strawberry.type
class DocumentBlock:
    """
    Document block for StreamField
    """

    id: uuid.UUID
    value: Optional[GenericScalar]

    @strawberry.field
    def document(self) -> Optional[DocumentNode]:
        return Document.objects.get(id=self.value)


@strawberry.type
class DocumentsQuery:
    """
    Document Query definition
    """

    @strawberry.field
    def document(self, pk: int) -> Optional[DocumentNode]:
        return Document.objects.get(pk=pk)

    @strawberry_django.connection(Connection[DocumentNode])
    def documents(self) -> Iterable[DocumentNode]:
        return Document.objects.all()
