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

from wagtail.rich_text import expand_db_html
from paskoocheh.media_storage import get_s3_url

from typing import NewType


def serialize(value):
    """
    Serialises RichText content into fully baked HTML
    see https://github.com/wagtail/wagtail/issues/2695#issuecomment-373002412
    """
    s3_url = get_s3_url()
    html = expand_db_html(value)
    if s3_url is not None:
        html = html.replace(s3_url, '')

    return html


RichTextFieldType = strawberry.scalar(
    NewType("RichTextFieldType", object),
    description="Serialises RichText content into fully baked HTML",
    serialize=lambda v: serialize(v),
    parse_value=lambda v: v,
)
