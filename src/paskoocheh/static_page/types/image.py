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
from typing import Optional, List, Iterable

from wagtail.images.models import Image

from static_page.types.tag import FlatTags
from static_page.types.generic import GenericScalar
from paskoocheh.media_storage import get_s3_url
from paskoocheh.utils import Connection


@strawberry.type
class ImageRendition:
    """
    Image rendition object
    """

    id: uuid.UUID
    url: Optional[str]
    width: Optional[int]
    height: Optional[int]


@strawberry.type
class ImageRenditionList:
    """
    A list of Image renditions
    """

    rendition_list: Optional[List[ImageRendition]]

    @strawberry.field
    def src_set(self) -> Optional[str]:
        return ", ".join(
            [f"{img.url} {img.width}w" for img in self.rendition_list])


@strawberry_django.type(Image, pagination=True)
class ImageNode(strawberry.relay.Node):
    """
    Relay: Images node
    """

    id: strawberry.relay.NodeID[int]
    # Define all available image rendition options as arguments
    focal_point_x: Optional[int]
    focal_point_y: Optional[int]
    focal_point_width: Optional[int]
    focal_point_height: Optional[int]
    width: int
    height: int
    file_size: Optional[int]
    file_hash: str
    title: str
    file: str
    created_at: datetime.datetime

    @strawberry.field
    def rendition(
        self,
        max: Optional[str] = strawberry.UNSET,
        min: Optional[str] = strawberry.UNSET,
        width: Optional[int] = strawberry.UNSET,
        height: Optional[int] = strawberry.UNSET,
        fill: Optional[str] = strawberry.UNSET,
        format: Optional[str] = strawberry.UNSET,
        bgcolor: Optional[str] = strawberry.UNSET,
        jpegquality: Optional[int] = strawberry.UNSET
    ) -> Optional[ImageRendition]:
        """
        Filters based on input arguments
        """

        rendition_fields = {}
        if max is not strawberry.UNSET:
            rendition_fields['max'] = max
        if min is not strawberry.UNSET:
            rendition_fields['min'] = min
        if width is not strawberry.UNSET:
            rendition_fields['width'] = width
        if height is not strawberry.UNSET:
            rendition_fields['height'] = height
        if fill is not strawberry.UNSET:
            rendition_fields['fill'] = fill
        if format is not strawberry.UNSET:
            rendition_fields['format'] = format
        if bgcolor is not strawberry.UNSET:
            rendition_fields['bgcolor'] = bgcolor
        if jpegquality is not strawberry.UNSET:
            rendition_fields['jpegquality'] = jpegquality

        filters = "|".join(
            [f"{key}-{val}" for key, val in rendition_fields.items()])

        img = self.get_rendition(filters)
        url = img.url
        s3_url = get_s3_url()
        if s3_url:
            url = url.replace(s3_url, '')

        return ImageRendition(
            id=img.id,
            url=url,
            width=img.width,
            height=img.height)

    @strawberry.field
    def rendition_list(
        self,
        sizes: Optional[List[Optional[int]]] = []
    ) -> Optional[ImageRenditionList]:
        """
        Create rendition list based on arguments
        """

        rendition_list = [
            ImageNode.rendition(self, width=width)
            for width in sizes
        ]

        return ImageRenditionList(rendition_list=rendition_list)

    @strawberry.field
    def tags(self) -> Optional[List[Optional[FlatTags]]]:
        return self.tags.all().order_by('slug')


@strawberry.type
class ImageBlock:
    """
    Image block for StreamField
    """

    id: uuid.UUID
    value: Optional[GenericScalar]

    @strawberry.field
    def image(self) -> Optional[ImageNode]:
        return Image.objects.get(id=self.value)


@strawberry.type
class ImageQuery:
    """
    Image Query definition
    """

    @strawberry.field
    def image(self, pk: int) -> Optional[ImageNode]:
        return Image.objects.get(pk=pk)

    @strawberry_django.connection(Connection[ImageNode])
    def images(self) -> Iterable[ImageNode]:
        return Image.objects.all()
