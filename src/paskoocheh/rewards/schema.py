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
from enum import Enum

import strawberry
from strawberry.relay.types import GlobalID
from strawberry.relay.utils import to_base64

import strawberry_django
from strawberry_django.auth.queries import get_current_user
from typing import Optional, List

from gqlauth.core.types_ import MutationNormalOutput

from django.contrib.auth import get_user_model
from wagtail.models import Locale

from paskoocheh.utils import Connection, IsAuthenticatedMutation
from static_page.types.generic import GenericBlock

from accounts.schema import MinimalUserNode

from rewards.models import (
    EarningMethod,
    RedemptionMethod,
    QuizPage,
    QuizResult,
    QuizzesIndexPage,
    ReferralLink)


User = get_user_model()


@strawberry.type
class AnswersBlock(GenericBlock):
    """
    Block to represent StructBlock for a single answer
    """

    @strawberry.field
    def answer(self) -> Optional[str]:
        return self.value['answer']

    @strawberry.field
    def correct(self) -> Optional[bool]:
        return self.value['correct']


@strawberry.type
class QuestionBlock(GenericBlock):
    """
    Block to represent StructBlock for a single question with answers
    """

    @strawberry.field
    def value(self) -> Optional[str]:
        return self.value['question']

    @strawberry.field
    def question(self) -> Optional[str]:
        return self.value['question']

    @strawberry.field
    def answers(self) -> Optional[List[AnswersBlock]]:
        return self.value['answers']


@strawberry.django.filters.filter(QuizPage, lookups=True)
class QuizFilter:
    title: strawberry.auto
    slug: strawberry.auto


@strawberry_django.type(QuizPage, pagination=True, filters=QuizFilter)
class QuizPageNode(strawberry.relay.Node):
    """
    Relay: Quiz Page Node
    """

    id: strawberry.relay.NodeID[int]
    pk: int
    title: str
    slug: str
    numchild: int
    url_path: str
    seo_title: str
    search_description: str

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        return queryset.live()

    @strawberry.field
    def questions(self) -> Optional[List[Optional[QuestionBlock]]]:
        return self.questions


@strawberry_django.type(QuizzesIndexPage, pagination=True)
class QuizIndexNode(strawberry.relay.Node):
    """
    Relay: Quizzes index page node
    """

    id: strawberry.relay.NodeID[int]
    pk: int
    title: str
    slug: str
    numchild: int
    url_path: str
    seo_title: str
    search_description: str
    description: str

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        return queryset.live()


@strawberry.enum
class RecordTypeEnum(Enum):
    EARNED = 'earn'
    REDEEMED = 'redeem'


@strawberry.type
class RewardsRecordType:
    """
    Relay: Rewards Record Type
    (merges UserRewardsRecord and AdminRewardsRecord)
    """

    @strawberry.field
    def id(self) -> GlobalID:
        # Description/pk combination will ensure uniqueness
        return to_base64(self.record_description, self.pk)

    @strawberry.field
    def record_type(self) -> RecordTypeEnum:
        return self.method_type

    @strawberry.field
    def points(self) -> int:
        return self.points

    @strawberry.field
    def description(self) -> str:
        return self.record_description

    @strawberry.field
    def date(self) -> datetime.date:
        return self.updated


@strawberry_django.type(ReferralLink, pagination=True)
class ReferralLinkNode(strawberry.relay.Node):
    """
    Relay: Referral Link Node
    """

    id: strawberry.relay.NodeID[int]
    pk: int
    referral_slug: str
    times_referred: int
    created: strawberry.auto
    updated: strawberry.auto

    @strawberry.field
    def user(self) -> Optional[MinimalUserNode]:
        return self.user


@strawberry_django.type(RedemptionMethod, pagination=True)
class RedemptionMethodNode(strawberry.relay.Node):
    """
    Relay: Redemption Method Node
    """

    id: strawberry.relay.NodeID[int]
    pk: int
    redemption_method_en: strawberry.auto
    redemption_method_fa: strawberry.auto
    redemption_points: strawberry.auto
    created: strawberry.auto
    updated: strawberry.auto


@strawberry_django.type(EarningMethod, pagination=True)
class EarningMethodNode(strawberry.relay.Node):
    """
    Relay: Earning Method Node
    """

    id: strawberry.relay.NodeID[int]
    pk: int
    earning_method: strawberry.auto
    earning_points: strawberry.auto
    created: strawberry.auto
    updated: strawberry.auto


@strawberry.type
class RewardsQuery:
    """
    Rewards Query
    """

    @strawberry.field
    def quiz_index(self, locale: str) -> Optional[QuizIndexNode]:
        quiz_index = None
        try:
            quiz_index = QuizzesIndexPage.objects.get(
                locale=Locale.objects.get(language_code=locale),
                live=True)
        except QuizzesIndexPage.DoesNotExist:
            pass
        return quiz_index

    @strawberry.field
    def quiz_indices(
        self,
        info: strawberry.types.Info,
        locale: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Optional[Connection[QuizIndexNode]]:
        quiz_indices = QuizzesIndexPage.objects.filter(
            locale=Locale.objects.get(language_code=locale))
        return Connection[QuizIndexNode].resolve_connection(
            info=info,
            nodes=quiz_indices,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def quiz(self, slug: str, locale: str) -> Optional[QuizPageNode]:
        quiz_page = None
        try:
            quiz_page = QuizPage.objects.get(
                slug=slug,
                locale=Locale.objects.get(language_code=locale),
                live=True)
        except QuizPage.DoesNotExist:
            return None
        return quiz_page

    @strawberry.field
    def quizzes(
        self,
        info: strawberry.types.Info,
        locale: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Optional[Connection[QuizPageNode]]:
        quizzes = QuizPage.objects\
            .filter(locale=Locale.objects.get(language_code=locale))\
            .order_by('-last_published_at')
        return Connection[QuizPageNode].resolve_connection(
            info=info,
            nodes=quizzes,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def redemption_methods(
        self,
        info: strawberry.types.Info,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Optional[Connection[RedemptionMethodNode]]:
        redemption_methods = RedemptionMethod.objects.all()
        return Connection[RedemptionMethodNode].resolve_connection(
            info=info,
            nodes=redemption_methods,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field
    def earning_methods(
        self
    ) -> Optional[List[EarningMethodNode]]:
        return EarningMethod.objects.all()


@strawberry.type
class RewardsMutation:
    """
    Rewards Mutation
    """

    @strawberry_django.mutation(extensions=[IsAuthenticatedMutation()])
    def report_quiz_results(
        self,
        info,
        quiz_pk: int,
        won: bool = False
    ) -> MutationNormalOutput:
        try:
            quiz = QuizPage.objects.get(
                pk=quiz_pk,
                live=True)
        except QuizPage.DoesNotExist:
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        'message': 'No published quiz was found',
                        'code': 'quiz_not_found'
                    }
                ]
            )
        try:
            user = get_current_user(info)
        except ValueError:
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        'message': 'No user found in the current request',
                        'code': 'user_not_found'
                    }
                ]
            )

        quiz_result, created = QuizResult.objects.get_or_create(
            quiz=quiz,
            user=user)

        if created:
            # Only earn points for newly completed quizzes
            if won:
                quiz_result.won = True
                quiz_result.save()
                user.profile.earn_quiz_won()
            else:
                user.profile.earn_quiz_completed()

        return MutationNormalOutput(
            success=True,
            errors=[])
