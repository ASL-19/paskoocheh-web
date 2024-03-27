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
import decimal
from enum import Enum

import json
import logging
import requests

import strawberry
import strawberry_django
from strawberry_django.auth.utils import get_request
from typing import Optional, List, Annotated, TYPE_CHECKING

from gqlauth.core.types_ import MutationNormalOutput

from paskoocheh.helpers import get_client_ip
from paskoocheh.utils import Connection, IsAuthenticatedMutation

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import validate_ipv46_address, validate_email
from django.core.exceptions import ValidationError

from stats.models import (
    VersionInstance,
    VersionDownload,
    VersionRating,
    VersionReview,
    RatingCategory,
    VersionCategoryRating,
    VersionReviewVote,
)
from tools.models import Version
from tools.utils import (
    get_object_by_tool_pk_or_slug,
    filter_objects_by_tool_pk_or_slug)
from stats.utils import save_download


logger = logging.getLogger(__name__)
User = get_user_model()


@strawberry.django.filters.filter(RatingCategory, lookups=True)
class RatingCategoryFilter:
    slug: strawberry.auto
    name: strawberry.auto


@strawberry_django.type(
    RatingCategory, pagination=True, filters=RatingCategoryFilter)
class RatingCategoryNode(strawberry.relay.Node):
    """
    Relay: Rating Category Node
    """

    id: strawberry.relay.NodeID[int]
    name: str
    name_fa: Optional[str]
    name_ar: Optional[str]
    slug: str


@strawberry.django.filters.filter(VersionInstance, lookups=True)
class VersionInstanceFilter:
    tool_name: strawberry.auto
    platform_name: strawberry.auto


@strawberry_django.type(
    VersionInstance, pagination=True, filters=VersionInstanceFilter)
class VersionInstanceNode(strawberry.relay.Node):
    """
    Relay: Version Instance Node
    """
    if TYPE_CHECKING:
        from tools.schema import ToolNode

    id: strawberry.relay.NodeID[int]
    last_modified: datetime.datetime
    tool_name: Optional[str]
    platform_name: Optional[str]

    @strawberry.field
    def tool(
        self
    ) -> Optional[Annotated['ToolNode', strawberry.lazy('tools.schema')]]:
        return self.tool


@strawberry.django.filters.filter(VersionRating, lookups=True)
class VersionRatingFilter(VersionInstanceFilter):
    star_rating: strawberry.auto
    rating_count: strawberry.auto


@strawberry_django.type(
    VersionRating, pagination=True, filters=VersionRatingFilter)
class VersionRatingNode(VersionInstanceNode):
    """
    Relay: Version Rating Node
    """

    id: strawberry.relay.NodeID[int]
    star_rating: decimal.Decimal
    rating_count: int


@strawberry.django.filters.filter(VersionDownload, lookups=True)
class VersionDownloadFilter(VersionInstanceFilter):
    download_count: strawberry.auto


@strawberry_django.type(
    VersionDownload, pagination=True, filters=VersionDownloadFilter)
class VersionDownloadNode(VersionInstanceNode):
    """
    Relay: Version Download Node
    """

    id: strawberry.relay.NodeID[int]
    download_count: int


@strawberry.django.filters.filter(VersionCategoryRating, lookups=True)
class VersionCategoryRatingFilter:
    star_rating: strawberry.auto


@strawberry_django.type(
    VersionCategoryRating,
    pagination=True,
    filters=VersionCategoryRatingFilter)
class VersionCategoryRatingNode(strawberry.relay.Node):
    """
    Relay: Version Category Rating Node
    """

    id: strawberry.relay.NodeID[int]
    star_rating: decimal.Decimal

    @strawberry.field
    def rating_category(self) -> Optional[RatingCategoryNode]:
        return self.rating_category


@strawberry.django.filters.filter(VersionReview, lookups=True)
class VersionReviewFilter(VersionInstanceFilter):
    rating: strawberry.auto
    language: strawberry.auto


@strawberry.enum
class ReviewVoteOptions(Enum):
    UPVOTE = 'upvote'
    DOWNVOTE = 'downvote'


@strawberry.type
class UserVote:
    has_voted: bool
    vote_type: Optional[ReviewVoteOptions]


@strawberry_django.type(
    VersionReview, pagination=True, filters=VersionReviewFilter)
class VersionReviewNode(VersionInstanceNode):
    """
    Relay: Version Review Node
    """

    id: strawberry.relay.NodeID[int]
    pk: int
    subject: Optional[str]
    user_id: Optional[str]
    text: Optional[str]
    username: Optional[str]
    rating: decimal.Decimal
    checked: bool
    tool_version: Optional[str]
    timestamp: datetime.datetime
    language: strawberry.auto

    @strawberry.field
    def category_ratings(self) -> List[VersionCategoryRatingNode]:
        return self.category_ratings.all()

    @strawberry.field
    def upvotes(self) -> int:
        return self.upvotes_count

    @strawberry.field
    def downvotes(self) -> int:
        return self.downvotes_count

    @strawberry.field
    def has_user_voted(self, username: str) -> UserVote:
        try:
            vote = VersionReviewVote.objects.get(
                user__username=username,
                review=self)
        except VersionReviewVote.DoesNotExist:
            return UserVote(has_voted=False, vote_type=None)
        except User.DoesNotExist:
            return UserVote(has_voted=False, vote_type=None)
        return UserVote(has_voted=True, vote_type=vote.vote)


@strawberry.type
class StatsQuery:
    """
    Stats Query
    """

    @strawberry.field
    def rating_category(self, slug: str) -> Optional[RatingCategoryNode]:
        try:
            category = RatingCategory.objects.get(
                slug=slug)
        except RatingCategory.DoesNotExist:
            return None
        return category

    @strawberry.field
    def rating_categories(
        self,
        info: strawberry.types.Info,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[RatingCategoryNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        rating_categories = RatingCategory.objects.all().order_by(*order)
        return Connection[RatingCategoryNode].resolve_connection(
            info=info,
            nodes=rating_categories,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def tool_average_rating(
        self,
        platform_slug: str,
        tool_pk: Optional[int] = None,
        tool_slug: Optional[str] = None
    ) -> Optional[VersionRatingNode]:
        filters = {
            'platform_name': platform_slug
        }
        try:
            rating = get_object_by_tool_pk_or_slug(
                VersionRating,
                tool_pk,
                tool_slug,
                **filters)
        except VersionRating.DoesNotExist:
            return None
        return rating

    @strawberry.field
    def tools_ratings(
        self,
        info: strawberry.types.Info,
        platform_slug: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[VersionRatingNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        ratings = VersionRating.objects.filter(
            platform_name=platform_slug).order_by(*order)
        return Connection[VersionRatingNode].resolve_connection(
            info=info,
            nodes=ratings,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def tool_total_downloads(
        self,
        platform_slug: str,
        tool_pk: Optional[int] = None,
        tool_slug: Optional[str] = None
    ) -> Optional[VersionDownloadNode]:
        filters = {
            'platform_name': platform_slug
        }
        try:
            download = get_object_by_tool_pk_or_slug(
                VersionDownload,
                tool_pk,
                tool_slug,
                **filters)
        except VersionDownload.DoesNotExist:
            return None
        return download

    @strawberry.field
    def tools_downloads(
        self,
        info: strawberry.types.Info,
        platform_slug: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[VersionDownloadNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        downloads = VersionDownload.objects.filter(
            platform_name=platform_slug).order_by(*order)
        return Connection[VersionDownloadNode].resolve_connection(
            info=info,
            nodes=downloads,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def user_reviews(
        self,
        info: strawberry.types.Info,
        username: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[VersionReviewNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        try:
            user = User.objects.get(
                username=username)
        except User.DoesNotExist:
            return Connection[VersionReviewNode].resolve_connection(
                info=info,
                nodes=VersionReview.objects.none(),
                offset=offset,
                first=first,
                last=last,
                after=after,
                before=before)
        version_reviews = VersionReview.objects.filter(
            pask_user=user).order_by(*order)
        return Connection[VersionReviewNode].resolve_connection(
            info=info,
            nodes=version_reviews,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def user_tool_reviews(
        self,
        info: strawberry.types.Info,
        username: str,
        tool_pk: Optional[int] = None,
        tool_slug: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[VersionReviewNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        try:
            user = User.objects.get(
                username=username)
        except User.DoesNotExist:
            return Connection[VersionReviewNode].resolve_connection(
                info=info,
                nodes=VersionReview.objects.none(),
                offset=offset,
                first=first,
                last=last,
                after=after,
                before=before)
        filters = {
            'pask_user': user
        }
        version_reviews = filter_objects_by_tool_pk_or_slug(
            VersionReview,
            tool_pk,
            tool_slug,
            **filters)
        if version_reviews:
            version_reviews = version_reviews.order_by(*order)
            return Connection[VersionReviewNode].resolve_connection(
                info=info,
                nodes=version_reviews,
                offset=offset,
                first=first,
                last=last,
                after=after,
                before=before)
        return Connection[VersionReviewNode].resolve_connection(
            info=info,
            nodes=VersionReview.objects.none(),
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def tool_reviews(
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
    ) -> Optional[Connection[VersionReviewNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        version_reviews = filter_objects_by_tool_pk_or_slug(
            VersionReview,
            tool_pk,
            tool_slug)
        if version_reviews:
            version_reviews = version_reviews.order_by(*order)
            return Connection[VersionReviewNode].resolve_connection(
                info=info,
                nodes=version_reviews,
                offset=offset,
                first=first,
                last=last,
                after=after,
                before=before)
        return Connection[VersionReviewNode].resolve_connection(
            info=info,
            nodes=VersionReview.objects.none(),
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def tools_reviews(
        self,
        info: strawberry.types.Info,
        platform_slug: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[List[Optional[str]]] = strawberry.UNSET,
    ) -> Optional[Connection[VersionReviewNode]]:
        order = [] if order_by is strawberry.UNSET else order_by
        reviews = VersionReview.objects.filter(
            platform_name=platform_slug).order_by(*order)
        return Connection[VersionReviewNode].resolve_connection(
            info=info,
            nodes=reviews,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)


@strawberry.input
class CategoryRatingInput:
    """
        To be used in writeReview mutation
    """
    category_slug: str
    rating: decimal.Decimal


@strawberry.enum
class DownloadOptions(Enum):
    S3 = 's3'
    APPLE_APP_STORE = 'apple-app-store'
    CHROME_WEB_STORE = 'chrome-web-store',
    GOOGLE_PLAY_STORE = 'google-play-store'
    MICROSOFT_STORE = 'microsoft-store'
    MOZILLA_ADDONS_DIRECTORY = 'mozilla-addons-directory'
    EXTERNAL_WEBSITE = 'external-website'


@strawberry.type
class StatsMutation:
    """
    Stats Mutations
    """
    @strawberry_django.mutation(extensions=[IsAuthenticatedMutation()])
    def write_review(
        self,
        info,
        rating: decimal.Decimal,
        language_code: str,
        version_pk: int,
        subject: Optional[str] = None,
        text: Optional[str] = None,
        categories_ratings: Optional[List[Optional[CategoryRatingInput]]] = [],
    ) -> MutationNormalOutput:
        """
        A mutation to write version reviews (user must be logged in and verified)
        """
        user = info.context.request.user

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

        if version not in user.profile.apps.all():
            error_code = 'version'
            error_message = 'Version not installed'
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
            review, created = VersionReview.objects.get_or_create(
                platform_name=version.supported_os.slug_name,
                tool_id=version.tool.pk,
                pask_user=user)
            # If a review exists, the user can update it
            review.subject = subject
            review.text = text
            review.rating = rating
            review.language = language_code
            review.tool_name = version.tool.name
            review.platform_name = version.supported_os.slug_name
            review.tool = version.tool
            review.tool_version = version.version_number
            # Run full_clean() to validate rating
            review.full_clean()
            review.save()

        except Exception:
            error_code = 'version_review'
            error_message = 'Could not create version review'
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        "message": error_message,
                        "code": error_code
                    }
                ]
            )

        if created:
            # Only earn points for newly added reviews
            user.profile.earn_review()

        for rating_input in categories_ratings:
            try:
                rating_category = RatingCategory.objects.get(slug=rating_input.category_slug)
            except RatingCategory.DoesNotExist:
                # We check for existing categories only
                continue
            version_category_rating, created = VersionCategoryRating.objects.get_or_create(
                version_review=review,
                rating_category=rating_category)
            version_category_rating.star_rating = rating_input.rating
            # Run full_clean() to validate rating
            version_category_rating.full_clean()
            version_category_rating.save(update_fields=['star_rating'])

        return MutationNormalOutput(
            success=True,
            errors=[])

    @strawberry_django.mutation(extensions=[IsAuthenticatedMutation()])
    def vote_review(
        self,
        info,
        review_pk: int,
        vote: ReviewVoteOptions
    ) -> MutationNormalOutput:
        """
        A mutation to vote other users reviews (user must be logged in and verified)
        """
        user = info.context.request.user

        try:
            review = VersionReview.objects.get(pk=review_pk)
        except VersionReview.DoesNotExist:
            error_code = 'review_not_found'
            error_message = 'Version review not found'
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        "message": error_message,
                        "code": error_code
                    }
                ]
            )

        if review.pask_user == user:
            error_code = 'own_review'
            error_message = 'Users can\'t vote their own reviews'
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        "message": error_message,
                        "code": error_code
                    }
                ]
            )

        else:
            try:
                # One vote per user/review
                review_vote = VersionReviewVote.objects.get(
                    review=review,
                    user=user)
                review_vote.vote = vote.value
                review_vote.save(update_fields=['vote'])
            except VersionReviewVote.DoesNotExist:
                VersionReviewVote.objects.create(
                    review=review,
                    user=user,
                    vote=vote.value)

        return MutationNormalOutput(
            success=True,
            errors=[])

    @strawberry.mutation
    def save_download(
        self,
        info,
        version_id: int,
        channel_version: str,
        downloaded_via: DownloadOptions,
    ) -> MutationNormalOutput:
        """
        A mutation to write version reviews (user must be logged in and verified)
        """
        try:
            request = get_request(info)
            request_ip = get_client_ip(request)
            validate_ipv46_address(request_ip)
        except ValidationError:
            error_code = 'invalid_ip'
            error_message = 'Request IP is not valid'
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
            Version.objects.get(pk=version_id)
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
            save_download(
                version_id=version_id,
                channel_version=channel_version,
                downloaded_via=downloaded_via.value,
                request_ip=request_ip.encode('utf-8'))

        except Exception as e:
            error_code = 'save_download'
            error_message = 'Could not save the download'
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
    def send_feedback(
        self,
        platform: str,
        email: str,
        message: str,
    ) -> MutationNormalOutput:
        """
        A mutation to send user feedback/message to helpdesk
        """

        try:
            validate_email(email)
        except ValidationError:
            error_code = 'invalid_email'
            error_message = 'Please provide a valid email address'
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        "message": error_message,
                        "code": error_code
                    }
                ]
            )
        ticket_endpoint = settings.HELPDESK_ENDPOINT
        token = settings.HELPDESK_API_TOKEN
        if not ticket_endpoint or not token:
            error_code = 'server_error'
            error_message = 'Please try again later'
            logger.error('Could not connect to helpdesk, check environment variables')
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        "message": error_message,
                        "code": error_code
                    }
                ]
            )
        headers = {
            'Authorization': f'Token {token}'
        }
        feedback = {
            'title': 'Paskoocheh Web Ticket',
            'group_id': settings.HELPDESK_USERS_GROUP_ID,
            'customer_id': f'guess:{email}',
            'article': {
                'subject': f'Ticket by {email} on {platform}',
                'body': f'{message}',
                'type': 'web',
                'internal': True
            }
        }
        response = requests.post(
            ticket_endpoint,
            headers=headers,
            data=json.dumps(feedback))
        if response.status_code != 201:
            error_code = 'feedback_failure'
            error_message = 'Could not send feedback'
            logger.error(f'Could not send feedback to helpdesk: Status code {response.status_code}')
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
