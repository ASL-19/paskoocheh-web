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
from strawberry.scalars import JSON

from typing import NewType


def serialize(value):
    return(
        {
            'name': value.name,
            'slug': value.slug
        }
    )


FlatTags = strawberry.scalar(
    NewType("FlatTags", JSON),
    description="",
    serialize=lambda v: serialize(v),
    parse_value=lambda v: v,
)
