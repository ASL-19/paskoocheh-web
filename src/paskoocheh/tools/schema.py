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

import logging
import datetime
import decimal
import markdown
from typing import List, Optional

import strawberry
import strawberry_django

from django.conf import settings
from django.core.exceptions import FieldError

from paskoocheh.utils import Connection, IsAuthenticatedMutation
from preferences.schema import PlatformNode, ToolTypeNode
from stats.schema import RatingCategoryNode

from gqlauth.core.types_ import MutationNormalOutput

from preferences.models import Platform
from tools.models import (CategoryAnalysis, Faq, Guide,
                          Image, Info, StepModel, TeamAnalysis, Tool, Tutorial,
                          HomeFeaturedTool, Version, ToolType)
from accounts.models import UserProfile
from stats.models import (
    VersionDownload, VersionRating, VersionReview)
from stats.schema import (
    VersionRatingNode, VersionReviewNode)
from tools.utils import (
    get_ordered_tools_by_platform,
    get_object_by_tool_pk_or_slug,
    filter_objects_by_tool_pk_or_slug)

from webfrontend.utils.general import get_temp_s3_url


logger = logging.getLogger(__name__)


@strawberry.django.filters.filter(Image, lookups=True)
class ImageFilter:
    language: strawberry.auto


@strawberry_django.type(Image, pagination=True, filters=ImageFilter)
class ToolImageNode(strawberry.relay.Node):
    """
    Relay: Tool Image Node
    """
    id: strawberry.relay.NodeID[int]
    pk: int
    last_modified: datetime.datetime
    image_type: Optional[str]
    width: Optional[int]
    height: Optional[int]
    should_display_full_bleed: bool
    order: int
    publish: bool
    language: strawberry.auto
    image: str


@strawberry.django.filters.filter(Tool, lookups=True)
class ToolFilter:
    opensource: strawberry.auto
    trusted: strawberry.auto
    featured: strawberry.auto


@strawberry_django.type(Tool, pagination=True, filters=ToolFilter)
class ToolNode(strawberry.relay.Node):
    """
    Relay: Tool Node
    """
    id: strawberry.relay.NodeID[int]
    pk: int
    last_modified: Optional[datetime.datetime]
    created: Optional[datetime.datetime]
    name: str
    last_update: Optional[datetime.datetime]
    trusted: bool
    featured: bool
    opensource: bool
    source: Optional[str]
    website: Optional[str]
    facebook: Optional[str]
    twitter: Optional[str]
    rss: Optional[str]
    blog: Optional[str]
    contact_email: Optional[str]
    contact_url: Optional[str]
    publishable: bool
    primary_tooltype: ToolTypeNode
    slug: str

    @strawberry.field
    def available_platforms(self) -> Optional[List[Optional[str]]]:
        versions = Version.objects.filter(
            publishable=True,
            tool=self).select_related('supported_os')
        return [version.supported_os.slug_name for version in versions]

    @strawberry.field
    def tool_types(self) -> Optional[List[Optional[ToolTypeNode]]]:
        return self.tooltype.all()

    @strawberry.field
    def images(self) -> Optional[List[Optional[ToolImageNode]]]:
        return self.images.filter(publish=True)

    @strawberry.field
    def versions(
        self,
        info: strawberry.types.Info,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection['VersionNode']]:
        order = [] if order_by is strawberry.UNSET else order_by
        versions = Version.objects.filter(
            publishable=True,
            tool=self).order_by(*order)
        return Connection['VersionNode'].resolve_connection(
            info=info,
            nodes=versions,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def team_analysis(self) -> Optional['TeamAnalysisNode']:
        try:
            team_analysis = TeamAnalysis.objects.get(
                tool=self,
                tool__publishable=True)
        except TeamAnalysis.DoesNotExist:
            return None
        return team_analysis

    @strawberry.field
    def faqs(
        self,
        info: strawberry.types.Info,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection['FaqNode']]:
        order = [] if order_by is strawberry.UNSET else order_by
        faqs = Faq.objects.filter(
            tool=self,
            tool__publishable=True).order_by(*order)
        return Connection['FaqNode'].resolve_connection(
            info=info,
            nodes=faqs,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def info(
        self,
        info: strawberry.types.Info,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection['InfoNode']]:
        order = [] if order_by is strawberry.UNSET else order_by
        tool_info = Info.objects.filter(
            publishable=True,
            tool=self,
            tool__publishable=True).order_by(*order)
        return Connection['InfoNode'].resolve_connection(
            info=info,
            nodes=tool_info,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)


@strawberry.django.filters.filter(Info, lookups=True)
class InfoFilter:
    language: strawberry.auto


@strawberry_django.type(Info, pagination=True, filters=InfoFilter)
class InfoNode(strawberry.relay.Node):
    """
    Relay: Info Node
    """
    id: strawberry.relay.NodeID[int]
    pk: int
    last_modified: datetime.datetime
    language: strawberry.auto
    name: str
    company: str
    publishable: bool
    tool: Optional[ToolNode]
    seo_description: strawberry.auto

    @strawberry.field
    def tool(self) -> Optional[ToolNode]:
        return self.tool

    @strawberry.field
    def description(self) -> Optional[str]:
        return markdown.markdown(self.description)

    @strawberry.field
    def promo_text(self) -> Optional[str]:
        try:
            featured_tool = HomeFeaturedTool.objects.get(tool=self.tool)
            if featured_tool.promo_text:
                return featured_tool.promo_text
            return None
        except HomeFeaturedTool.DoesNotExist:
            return None


@strawberry_django.type(Version, pagination=True)
class VersionNode(strawberry.relay.Node):
    """
    Relay: Version Node
    """
    id: strawberry.relay.NodeID[int]
    pk: int
    last_modified: datetime.datetime
    created: Optional[datetime.datetime]
    version_number: str
    release_date: datetime.datetime
    release_jdate: str
    download_url: Optional[str]
    release_url: Optional[str]
    package_name: Optional[str]
    auto_update: bool
    permissions: Optional[str]
    guide_url: Optional[str]
    faq_url: str
    publishable: bool
    video: Optional[str]
    video_link: Optional[str]
    is_bundled_app: bool
    tool: Optional[ToolNode]
    platform: Optional[PlatformNode]
    delivery_email: str

    @strawberry.field
    def tool(self) -> Optional[ToolNode]:
        return self.tool

    @strawberry.field
    def platform(self) -> Optional[PlatformNode]:
        return self.supported_os

    @strawberry.field
    def can_generate_temp_s3_url(self) -> bool:
        # Checks if we have a key for the app in S3
        if not self.version_codes:
            return False
        version_code = self.version_codes.first()
        if version_code and version_code.s3_key:
            return True
        return False

    @strawberry.field
    def guides(
        self,
        info: strawberry.types.Info,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection['GuideNode']]:
        order = [] if order_by is strawberry.UNSET else order_by

        guides = Guide.objects.filter(
            version=self,
            publishable=True).order_by(*order)
        return Connection['GuideNode'].resolve_connection(
            info=info,
            nodes=guides,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def tutorials(
        self,
        info: strawberry.types.Info,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection['TutorialNode']]:
        order = [] if order_by is strawberry.UNSET else order_by
        tutorials = Tutorial.objects.filter(
            publishable=True,
            version=self).order_by(*order)
        return Connection['TutorialNode'].resolve_connection(
            info=info,
            nodes=tutorials,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def download_count(
        self
    ) -> Optional[int]:
        try:
            download = VersionDownload.objects.get(
                tool=self.tool,
                platform_name=self.supported_os.slug_name).download_count
        except VersionDownload.DoesNotExist:
            return None
        return download

    @strawberry.field
    def average_rating(
        self,
    ) -> Optional[VersionRatingNode]:
        try:
            rating = VersionRating.objects.get(
                tool=self.tool,
                platform_name=self.supported_os.slug_name)
        except VersionRating.DoesNotExist:
            return None
        return rating

    @strawberry.field
    def reviews(
        self,
        info: strawberry.types.Info,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET
    ) -> Optional[Connection[VersionReviewNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        reviews = VersionReview.objects.filter(
            tool=self.tool,
            platform_name=self.supported_os.slug_name).order_by(*order)
        return Connection[VersionReviewNode].resolve_connection(
            info=info,
            nodes=reviews,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)


@strawberry.django.filters.filter(StepModel, lookups=True)
class StepModelFilter:
    language: strawberry.auto


@strawberry_django.type(StepModel, pagination=True, filters=StepModelFilter)
class StepNode(strawberry.relay.Node):
    """
    Relay: Step Node
    """
    id: strawberry.relay.NodeID[int]
    pk: int
    last_modified: datetime.datetime
    language: strawberry.auto
    headline: Optional[str]
    order: Optional[int]
    publishable: bool
    version: Optional[VersionNode]

    @strawberry.field
    def version(self) -> Optional[VersionNode]:
        return self.version

    @strawberry.field
    def body(self) -> Optional[str]:
        return markdown.markdown(self.body)


@strawberry.django.filters.filter(Faq, lookups=True)
class FaqFilter:
    language: strawberry.auto


@strawberry_django.type(Faq, pagination=True, filters=FaqFilter)
class FaqNode(StepNode):
    """
    Relay: FAQ Node
    """
    id: strawberry.relay.NodeID[int]
    pk: int
    tool: Optional[ToolNode]
    click_count: int
    video: Optional[str]
    version: Optional[VersionNode]

    @strawberry.field
    def version(self) -> Optional[VersionNode]:
        return self.version

    @strawberry.field
    def tool(self) -> Optional[ToolNode]:
        return self.tool


@strawberry.django.filters.filter(Guide, lookups=True)
class GuideFilter:
    language: strawberry.auto


@strawberry_django.type(Guide, pagination=True, filters=GuideFilter)
class GuideNode(StepNode):
    """
    Relay: Guide Node
    """
    id: strawberry.relay.NodeID[int]
    pk: int
    slug: Optional[str]
    video: Optional[str]
    version: Optional[VersionNode]

    @strawberry.field
    def version(self) -> Optional[VersionNode]:
        return self.version


@strawberry.django.filters.filter(Tutorial, lookups=True)
class TutorialFilter:
    language: strawberry.auto


@strawberry_django.type(Tutorial, pagination=True, filters=TutorialFilter)
class TutorialNode(strawberry.relay.Node):
    """
    Relay: Tutorial Node
    """
    id: strawberry.relay.NodeID[int]
    pk: int
    last_modified: datetime.datetime
    language: strawberry.auto
    video: Optional[str]
    video_link: Optional[str]
    title: str
    order: int
    publishable: bool

    @strawberry.field
    def version(self) -> Optional[VersionNode]:
        return self.version


@strawberry.django.filters.filter(CategoryAnalysis, lookups=True)
class CategoryAnalysisFilter:
    rating: strawberry.auto


@strawberry_django.type(
    CategoryAnalysis, pagination=True, filters=CategoryAnalysisFilter)
class CategoryAnalysisNode(strawberry.relay.Node):
    """
    Relay: Category Analysis Node
    """
    id: strawberry.relay.NodeID[int]
    pk: int
    rating: decimal.Decimal

    @strawberry.field
    def rating_category(self) -> Optional[RatingCategoryNode]:
        return self.rating_category


@strawberry_django.type(TeamAnalysis, pagination=True)
class TeamAnalysisNode(strawberry.relay.Node):
    """
    Relay: Team Analysis Node
    """
    id: strawberry.relay.NodeID[int]
    pk: int
    review: Optional[str]
    pros: Optional[str]
    cons: Optional[str]

    @strawberry.field
    def tool(self) -> Optional[ToolNode]:
        return self.tool

    @strawberry.field
    def category_analysis(
        self
    ) -> Optional[List[Optional[CategoryAnalysisNode]]]:
        return self.team_categoryratings.all()


@strawberry.input
class OrderByPlatformInput:
    platform_slug: str
    order_by: str


@strawberry.type
class ToolsQuery:
    """
    Tools Query
    """

    @strawberry.field
    def tool(
        self,
        pk: Optional[int] = None,
        slug: Optional[str] = None
    ) -> Optional[ToolNode]:
        if pk and slug:
            return None
        elif pk:
            try:
                tool = Tool.objects.get(
                    pk=pk,
                    publishable=True)
                return tool
            except Tool.DoesNotExist:
                return None
        elif slug:
            try:
                tool = Tool.objects.get(
                    slug=slug,
                    publishable=True)
                return tool
            except Tool.DoesNotExist:
                return None
        else:
            return None

    @strawberry.field
    def home_page_featured_tool(self) -> Optional[ToolNode]:
        try:
            featured_tool = HomeFeaturedTool.objects.get()
            if featured_tool:
                return featured_tool.tool
            return None
        except HomeFeaturedTool.DoesNotExist:
            return None

    @strawberry.field
    def tools(
        self,
        info: strawberry.types.Info,
        order_by_platform: Optional[OrderByPlatformInput] = strawberry.UNSET,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[ToolNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        if order_by_platform is not strawberry.UNSET:
            tools = get_ordered_tools_by_platform(
                order_by_platform.platform_slug,
                order_by_platform.order_by)
        else:
            tools = Tool.objects.filter(
                publishable=True).prefetch_related().order_by(*order)
        return Connection[ToolNode].resolve_connection(
            info=info,
            nodes=tools,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def version(
        self,
        platform_slug: str,
        tool_pk: Optional[int] = None,
        tool_slug: Optional[str] = None
    ) -> Optional[VersionNode]:
        filters = {
            'tool__publishable': True,
            'publishable': True,
            'supported_os__slug_name': platform_slug
        }
        try:
            version = get_object_by_tool_pk_or_slug(
                Version,
                tool_pk,
                tool_slug,
                **filters)
        except Version.DoesNotExist:
            return None
        return version

    @strawberry.field
    def versions(  # noqa C901
        self,
        info: strawberry.types.Info,
        tool_pk: Optional[int] = strawberry.UNSET,
        featured: Optional[bool] = False,
        platform_slug: Optional[str] = strawberry.UNSET,
        category: Optional[str] = strawberry.UNSET,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[VersionNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        order_by_field = None
        if order and order[0] in [
                'download_count',
                '-download_count',
                'star_rating',
                '-star_rating']:
            order_by_field = order[0]
        filters = {
            'tool__publishable': True,
            'publishable': True
        }
        if category is not strawberry.UNSET:
            try:
                filters['tool__tooltype'] = ToolType.objects.get(slug=category)
            except ToolType.DoesNotExist:
                return Connection[VersionNode].resolve_connection(
                    info=info,
                    nodes=Version.objects.none(),
                    offset=offset,
                    first=first,
                    last=last,
                    after=after,
                    before=before)
        if featured:
            filters['tool__featured'] = True
        if tool_pk is not strawberry.UNSET:
            filters['tool_id'] = tool_pk
        elif platform_slug is not strawberry.UNSET:
            supported_os = Platform.objects.get(slug_name=platform_slug)
            filters['supported_os'] = supported_os
            if order_by_field is not None:
                tools = get_ordered_tools_by_platform(
                    platform_slug,
                    order_by_field)
                versions = []
                for tool in tools:
                    try:
                        version = Version.objects.get(
                            tool=tool,
                            **filters)
                        versions.append(version)
                    except Version.DoesNotExist:
                        continue
                    except Version.MultipleObjectsReturned:
                        versions.append(
                            Version.objects.filter(
                                tool=tool,
                                **filters)
                            .order_by('-last_modified').first())
                return Connection[VersionNode].resolve_connection(
                    info=info,
                    nodes=versions,
                    offset=offset,
                    first=first,
                    last=last,
                    after=after,
                    before=before)
        versions = Version.objects.filter(**filters).distinct().order_by(*order)
        return Connection[VersionNode].resolve_connection(
            info=info,
            nodes=versions,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def temp_s3_url(
        self,
        version_pk: int
    ) -> Optional[str]:
        try:
            version = Version.objects.get(
                pk=version_pk,
                publishable=True,
                tool__publishable=True)
        except Version.DoesNotExist:
            return None
        try:
            link = get_temp_s3_url(version)
        except FieldError:
            return None
        if not link:
            return None
        return f'https://{settings.AWS_S3_CUSTOM_DOMAIN}{link}'

    @strawberry.field
    def team_analysis(
        self,
        tool_pk: Optional[int] = None,
        tool_slug: Optional[str] = None
    ) -> Optional[TeamAnalysisNode]:
        filters = {
            'tool__publishable': True
        }
        try:
            team_analysis = get_object_by_tool_pk_or_slug(
                TeamAnalysis,
                tool_pk,
                tool_slug,
                **filters)
        except TeamAnalysis.DoesNotExist:
            return None
        return team_analysis

    @strawberry.field
    def faqs(
        self,
        info: strawberry.types.Info,
        tool_pk: Optional[int] = None,
        tool_slug: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[FaqNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        filters = {
            'tool__publishable': True
        }
        faqs = filter_objects_by_tool_pk_or_slug(
            Faq,
            tool_pk,
            tool_slug,
            **filters)
        if faqs:
            faqs = faqs.order_by(*order)
        else:
            faqs = Faq.objects.none()
        return Connection[FaqNode].resolve_connection(
            info=info,
            nodes=faqs,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def guides(
        self,
        info: strawberry.types.Info,
        platform_slug: str,
        tool_pk: Optional[int] = None,
        tool_slug: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[GuideNode]]:
        order = [] if order_by is strawberry.UNSET else order_by

        try:
            platform = Platform.objects.get(
                slug_name=platform_slug)
        except Platform.DoesNotExist:
            guides = Guide.objects.none()
            return Connection[GuideNode].resolve_connection(
                info=info,
                nodes=guides,
                offset=offset,
                first=first,
                last=last,
                after=after,
                before=before)

        filters = {
            'publishable': True,
            'tool__publishable': True,
            'supported_os': platform
        }
        try:
            version = get_object_by_tool_pk_or_slug(
                Version,
                tool_pk,
                tool_slug,
                **filters)
        except Version.DoesNotExist:
            guides = Guide.objects.none()
            return Connection[GuideNode].resolve_connection(
                info=info,
                nodes=guides,
                offset=offset,
                first=first,
                last=last,
                after=after,
                before=before)

        if version:
            guides = Guide.objects.filter(
                version=version,
                publishable=True).order_by(*order)
        else:
            guides = Guide.objects.none()
        return Connection[GuideNode].resolve_connection(
            info=info,
            nodes=guides,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def tutorials(
        self,
        info: strawberry.types.Info,
        platform_slug: str,
        tool_pk: Optional[int] = None,
        tool_slug: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[TutorialNode]]:
        order = [] if order_by is strawberry.UNSET else order_by

        try:
            platform = Platform.objects.get(
                slug_name=platform_slug)
        except Platform.DoesNotExist:
            tutorials = Tutorial.objects.none()
            return Connection[TutorialNode].resolve_connection(
                info=info,
                nodes=tutorials,
                offset=offset,
                first=first,
                last=last,
                after=after,
                before=before)

        filters = {
            'publishable': True,
            'tool__publishable': True,
            'supported_os': platform
        }
        try:
            version = get_object_by_tool_pk_or_slug(
                Version,
                tool_pk,
                tool_slug,
                **filters)
        except Version.DoesNotExist:
            tutorials = Tutorial.objects.none()
            return Connection[TutorialNode].resolve_connection(
                info=info,
                nodes=tutorials,
                offset=offset,
                first=first,
                last=last,
                after=after,
                before=before)

        if version:
            tutorials = Tutorial.objects.filter(
                publishable=True,
                version=version).order_by(*order)
        else:
            tutorials = Tutorial.objects.none()
        return Connection[TutorialNode].resolve_connection(
            info=info,
            nodes=tutorials,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def info(
        self,
        info: strawberry.types.Info,
        tool_pk: Optional[int] = None,
        tool_slug: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[InfoNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        filters = {
            'publishable': True,
            'tool__publishable': True
        }
        tool_info = filter_objects_by_tool_pk_or_slug(
            Info,
            tool_pk,
            tool_slug,
            **filters)
        if tool_info:
            tool_info = tool_info.order_by(*order)
        else:
            tool_info = Info.objects.none()
        return Connection[InfoNode].resolve_connection(
            info=info,
            nodes=tool_info,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)


@strawberry.type
class ToolsMutation:
    """
    Tools Mutations
    """

    @strawberry_django.mutation(extensions=[IsAuthenticatedMutation()])
    def install_or_update_app(
        self,
        info,
        version_pk: int
    ) -> MutationNormalOutput:

        try:
            user = UserProfile.objects.get(
                user=info.context.request.user)
        except UserProfile.DoesNotExist:
            error_code = 'user'
            error_message = 'User not found'
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        "message": error_message,
                        "code": error_code
                    }
                ]
            )

        try:
            version = Version.objects.get(pk=version_pk)
        except Version.DoesNotExist:
            error_code = 'version'
            error_message = 'Version not found'
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        "message": error_message,
                        "code": error_code
                    }
                ]
            )

        try:
            user.install_or_update_app(version)
        except Exception as e:
            error_code = 'user_apps'
            error_message = 'Could not add app to user apps'
            logger.error(f'save_download mutation failed with code: {error_code} and error: {e}')
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        "message": error_message,
                        "code": error_code
                    }
                ]
            )

        return MutationNormalOutput(
            success=True,
            errors=[])

    @strawberry.mutation
    def increment_click_count(
        self,
        faq_pk: int
    ) -> MutationNormalOutput:
        # We will update click count using Queryset.update() to not send a
        # `post_save` signal that will trigger cloudfront invalidation
        faq = Faq.objects.filter(pk=faq_pk)
        if faq:
            faq.update(click_count=faq.first().click_count + 1)
        else:
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        "message": "FAQ not found",
                        "code": "faq_not_found"
                    }
                ]
            )

        return MutationNormalOutput(
            success=True,
            errors=[])
