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
from strawberry_django.optimizer import DjangoOptimizerExtension
from strawberry.extensions import AddValidationRules
from graphql.validation import NoSchemaIntrospectionCustomRule

from django.conf import settings

from accounts.schema import UserQuery, UserMutation

from tools.schema import (
    ToolsQuery,
    ToolsMutation,
)

from blog_wagtail.schema import BlogQuery
from static_page.schema import StaticPageQuery
from static_page.types.captioned_image import CaptionedImageQuery
from static_page.types.document import DocumentsQuery
from static_page.types.embed import EmbedQuery
from static_page.types.image import ImageQuery
from rewards.schema import RewardsQuery, RewardsMutation
from preferences.schema import PreferencesQuery
from stats.schema import StatsQuery, StatsMutation


@strawberry.type
class Query(
    UserQuery,
    BlogQuery,
    StaticPageQuery,
    RewardsQuery,
    ToolsQuery,
    StatsQuery,
    PreferencesQuery,
    CaptionedImageQuery,
    DocumentsQuery,
    ImageQuery,
    EmbedQuery
):
    pass


@strawberry.type
class Mutation(
        RewardsMutation,
        ToolsMutation,
        StatsMutation,
        UserMutation):
    pass


extensions = [
    DjangoOptimizerExtension,
]

# Disable Introspection in production
if settings.BUILD_ENV == 'production':
    extensions.append(AddValidationRules([NoSchemaIntrospectionCustomRule]))


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=extensions)
