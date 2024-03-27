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

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from paskoocheh.models import DatesMixin

from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail.admin.panels import FieldPanel


User = get_user_model()


REWARDS_EARNING_METHODS = [
    ('review', 'App Review'),
    ('quiz_completed', 'Weekly Challenge Completed'),
    ('quiz_won', 'Weekly Challenge Won'),
    ('update', 'Apps Update'),
    ('referral', 'Friend\'s Referral'),
]


class QuizzesIndexPage(Page):
    """
    Quizzes (Weekly Challenges) index page
    """

    description = RichTextField()

    subpage_types = [
        'QuizPage',
    ]

    # Only allowed to be created under root
    parent_page_types = [
        Page,
    ]

    search_fields = Page.search_fields + [
        index.SearchField('description'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('description', classname='full'),
    ]

    max_count_per_parent = len(settings.LANGUAGES)


class AnswerBlock(blocks.StructBlock):
    """
    Answer block definition (StructBlock)
    to be used for each question StreamBlock in quizzes
    """

    answer = blocks.CharBlock()

    correct = blocks.BooleanBlock(required=False)


class QuestionBlock(blocks.StructBlock):
    """
    Question block definition (StreamBlock)
    """

    question = blocks.TextBlock()

    answers = blocks.StreamBlock([
        ('answer', AnswerBlock(icon='comment')),
    ])


class QuizPage(Page):
    """
    Quiz (Weekly Challenge) page model definition
    """

    questions = StreamField([
        ('question', QuestionBlock(icon='help'))
    ], use_json_field=True)

    # Only allowed to be created under QuizzesIndexPage
    parent_page_types = [
        'QuizzesIndexPage'
    ]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('questions'),
    ]


class QuizResult(models.Model):
    """
    Quiz result used to decide if users should get points
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quizzes')

    quiz = models.ForeignKey(
        QuizPage,
        on_delete=models.SET_NULL,
        null=True,
        related_name='results')

    completed = models.DateTimeField(
        auto_now_add=True)

    won = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'quiz')

    def __str__(self):
        return f'{self.user} ({self.quiz})'


class ReferralLink(DatesMixin):
    """
    Referral Link model definition
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='referral_links')

    referral_slug = models.SlugField(max_length=64)

    times_referred = models.PositiveIntegerField(
        default=0)

    def __str__(self):
        return f'{self.user} ({self.times_referred} referrals)'


class EarningMethod(DatesMixin):
    """
    Earning method model definition
    """
    earning_method = models.CharField(
        unique=True,
        max_length=200,
        choices=REWARDS_EARNING_METHODS)

    earning_points = models.PositiveIntegerField(
        default=0)

    def __str__(self):
        return f'{self.earning_method}'


class RedemptionMethod(DatesMixin):
    """
    Redemption method model definition
    """
    redemption_method_en = models.CharField(
        unique=True,
        max_length=200)

    redemption_method_fa = models.CharField(
        unique=True,
        max_length=200)

    redemption_points = models.PositiveIntegerField(
        default=0)

    def __str__(self):
        return f'{self.redemption_method_en}'


class UserRewardsRecord(DatesMixin):
    """
    Individual record - for each reward earned - model definition
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rewards_records')

    earning_method = models.ForeignKey(
        EarningMethod,
        on_delete=models.CASCADE,
        related_name='rewards_records')

    class Meta:
        verbose_name = 'User Rewards Record'
        verbose_name_plural = 'Users Rewards Records'

    def __str__(self):
        return f'{self.user} ({self.earning_method})'


class AdminRewardsRecord(DatesMixin):
    """
    Individual record - for each reward earned - model definition
    """
    admin = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        limit_choices_to={'is_staff': True},
        related_name='user_rewards')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='admin_rewards')

    method_type = models.CharField(
        max_length=10,
        choices=(
            ('earn', 'Earn'),
            ('redeem', 'Redeem'),
        ))

    points = models.PositiveIntegerField(
        default=0)

    description = models.CharField(
        max_length=250)

    class Meta:
        verbose_name = 'Admin Rewards Record'
        verbose_name_plural = 'Admin Rewards Records'

    def __str__(self):
        return f'{self.user} ({self.description})'
