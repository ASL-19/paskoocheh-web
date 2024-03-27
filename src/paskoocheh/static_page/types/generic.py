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
import strawberry
from typing import NewType, Any, Optional


GenericScalar = strawberry.scalar(
    NewType("GenericScalar", Any),
    description="The GenericScalar scalar type represents a generic GraphQL scalar value that could be: List or Object."
)


@strawberry.type
class GenericBlock:
    """
    Generic block representation
    """
    id: uuid.UUID
    value: Optional[GenericScalar]
