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

import markdown
import strawberry

from typing import Optional

from static_page.types.generic import GenericBlock
from static_page.types.richtext import RichTextFieldType


@strawberry.type
class TextBlock(GenericBlock):

    @strawberry.field
    def text(self) -> Optional[RichTextFieldType]:
        return self.value


@strawberry.type
class MarkdownBlock(GenericBlock):

    @strawberry.field
    def markdown(self) -> Optional[RichTextFieldType]:
        return self.value

    @strawberry.field
    def html(self) -> Optional[RichTextFieldType]:
        return markdown.markdown(self.value)


@strawberry.type
class CollapsibleBlock(GenericBlock):

    @strawberry.field
    def slug(self) -> Optional[str]:
        return self.value['slug']

    @strawberry.field
    def heading(self) -> Optional[str]:
        return self.value['heading']

    @strawberry.field
    def text(self) -> Optional[RichTextFieldType]:
        return self.value['text']
