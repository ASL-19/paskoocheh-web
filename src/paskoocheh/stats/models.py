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
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from paskoocheh.helpers import SingletonModel
from tools.models import Tool
from webfrontend.caches.responses.signal_handlers import purge_versionreview


User = get_user_model()


class StatsLastRecords(SingletonModel):
    """
        Last records that we gather information from.
        This is to make sure we don't count duplicate records
    """

    download_last = models.IntegerField(
        default=0)
    failed_last = models.IntegerField(
        default=0)
    install_last = models.IntegerField(
        default=0)
    update_last = models.IntegerField(
        default=0)
    feedback_last = models.IntegerField(
        default=0)
    rating_last = models.IntegerField(
        default=0)
    review_last = models.IntegerField(
        default=0)


class RatingCategory(models.Model):
    """
        Individual categories used to rate tools in
    """

    name = models.CharField(
        max_length=100)
    name_fa = models.CharField(
        max_length=100)
    name_ar = models.CharField(
        max_length=100,
        null=True,
        blank=True)
    slug = models.SlugField(
        unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Rating Categories'


class VersionInstance(models.Model):
    """
        VersionInstance as a base model to keep track of
        downloads and reviews that need to reference the
        versions of tools
    """

    last_modified = models.DateTimeField(
        verbose_name=_('Last modified time'),
        auto_now=True)
    tool_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_('Tool name'))
    platform_name = models.CharField(
        max_length=128,
        verbose_name=_('Platform Name'),
        null=True,
        blank=True)
    tool = models.ForeignKey(
        Tool,
        verbose_name=_('Tool'),
        null=False,
        blank=False,
        on_delete=models.CASCADE)

    class Meta:

        abstract = True


class VersionRating(VersionInstance):
    """
        Ratings model to keep track of ratings
        of versions of tools
    """

    star_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        verbose_name=_('Star Rating'),
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)],
        default=2.5)
    rating_count = models.PositiveIntegerField(
        default=0)

    def __str__(self):

        return self.tool_name + ' ' + self.platform_name


class VersionDownload(VersionInstance):
    """
        Download model to keep track of number of downloads
        of versions of tools
    """

    download_count = models.PositiveIntegerField(
        default=0)

    def __str__(self):

        return self.tool_name + ' ' + self.platform_name


class VersionReview(VersionInstance):
    """
        Review model to keep track of reviews for each version
    """
    subject = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_('Subject'))
    user_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('User Name'))
    text = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Text'))
    username = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_('User Name'))
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        verbose_name=_('Star Rating'),
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)],
        default=2.5)
    checked = models.BooleanField(
        default=True,
        verbose_name=_('Checked'))
    tool_version = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_('Tool Version'))
    timestamp = models.DateTimeField(
        null=False,
        blank=False,
        default=timezone.now)
    language = models.CharField(
        max_length=2,
        default=settings.LANGUAGE_SUPPORTED_DEFAULT,
        choices=settings.LANGUAGE_SUPPORTED_CHOICES,
        verbose_name=_('Language'))
    pask_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True)

    def __str__(self):
        if self.tool_name and self.platform_name:
            return self.tool_name + ' ' + self.platform_name
        elif self.tool_name:
            return self.tool_name
        else:
            return ''

    @property
    def upvotes_count(self):
        return self.votes.filter(vote='upvote').count()

    @property
    def downvotes_count(self):
        return self.votes.filter(vote='downvote').count()


class VersionReviewVote(models.Model):
    """
        Version review vote model definition
    """

    VOTE_CHOICES = (
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    )

    review = models.ForeignKey(
        VersionReview,
        related_name='votes',
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        related_name='votes',
        null=True,
        on_delete=models.SET_NULL)
    vote = models.CharField(
        max_length=8,
        choices=VOTE_CHOICES)

    def __str__(self):
        return f'{str(self.review)}({self.vote})'


class VersionCategoryRating(models.Model):
    """
        Ratings model to keep track of category ratings
        of versions of tools
    """

    version_review = models.ForeignKey(
        VersionReview,
        related_name='category_ratings',
        on_delete=models.CASCADE)
    rating_category = models.ForeignKey(
        RatingCategory,
        related_name='user_ratings',
        on_delete=models.CASCADE)
    star_rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        verbose_name=_('Star Rating'),
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)],
        default=2.5)

    def __str__(self):

        return str(self.version_review) + ' ' + str(self.rating_category)


post_save.connect(purge_versionreview, sender=VersionReview)
post_delete.connect(purge_versionreview, sender=VersionReview)


class Feedback(models.Model):
    """
        Feedback model to hold users feedback
    """

    FEEDBACK_STATUS_CHOICES = (
        ('0', 'New'),
        ('1', 'Read'),
        ('2', 'Purged')
    )

    last_modified = models.DateTimeField(
        verbose_name=_('Last modified time'),
        auto_now=True)
    created = models.DateTimeField(
        verbose_name=_('Creation Date'),
        auto_now_add=True)
    user_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('User Name'))
    title = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_('Subject'))
    text = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        verbose_name=_('Message'))
    timestamp = models.DateTimeField(
        null=False,
        blank=False,
        default=timezone.now)
    channel = models.CharField(
        max_length=32,
        choices=settings.PASKOOCHEH_CHANNEL_CHOICES)
    channel_version = models.CharField(
        max_length=128,
        verbose_name=_('Channel Version'))
    platform_name = models.CharField(
        max_length=128,
        verbose_name=_('Platform Name'),
        null=True,
        blank=True)
    platform_version = models.CharField(
        max_length=128,
        verbose_name=_('Platform Version'),
        null=True,
        blank=True)
    status = models.CharField(
        choices=FEEDBACK_STATUS_CHOICES,
        max_length=2,
        null=False,
        blank=False,
        verbose_name=_('Status'),
        default='0')

    def __str__(self):

        return self.title
