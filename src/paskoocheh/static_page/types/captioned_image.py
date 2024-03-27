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

from paskoocheh.utils import Connection

from static_page.models import CaptionedImage

from static_page.types.image import ImageNode, ImageBlock

from typing import Optional, Iterable


@strawberry_django.type(CaptionedImage, pagination=True)
class CaptionedImageNode(ImageNode):
    """
    Relay: Captioned Images node
    """

    id: strawberry.relay.NodeID[int]
    pk: int
    caption: str
    credit: str


@strawberry.type
class CaptionedImageBlock(ImageBlock):
    """
    CaptionedImage block for StreamField
    """

    @strawberry.field
    def image(self) -> Optional[CaptionedImageNode]:
        return CaptionedImage.objects.get(id=self.value)


@strawberry.type
class CaptionedImageQuery:
    """
    Captioned Image Query definition
    """

    @strawberry.field
    def captioned_image(self, pk: int) -> Optional[CaptionedImageNode]:
        return CaptionedImage.objects.get(pk=pk)

    @strawberry_django.connection(Connection[CaptionedImageNode])
    def captioned_images(self) -> Iterable[CaptionedImageNode]:
        return CaptionedImage.objects.all()
