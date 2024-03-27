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


from django.contrib import admin
from .models import (
    VersionReview,
    VersionRating,
    VersionDownload,
    Feedback,
    RatingCategory,
    VersionCategoryRating,
    VersionReviewVote,
)
from paskoocheh.helpers import ReadOnlyAdmin


@admin.register(VersionDownload)
class VersionDownloadAdmin(ReadOnlyAdmin):
    """
        VersionDownload view admin panel
    """

    list_display = [
        'tool_name',
        'platform_name',
        'download_count'
    ]

    search_fields = [
        'tool_name',
        'platform_name'
    ]

    def save_model(self, request, obj):
        pass


@admin.register(VersionRating)
class VersionRatingAdmin(ReadOnlyAdmin):
    """
        VersionRating view admin panel
    """

    list_display = [
        'tool_name',
        'platform_name',
        'star_rating',
        'rating_count'
    ]

    search_fields = [
        'tool_name',
        'platform_name'
    ]

    def save_model(self, request, obj):
        pass


class VersionCategoryRatingAdmin(ReadOnlyAdmin):
    """
        Version Rating Category add/edit admin panel
    """

    list_display = [field.name for field in VersionCategoryRating._meta.get_fields()]


@admin.register(RatingCategory)
class RatingCategoryAdmin(admin.ModelAdmin):
    """
        Rating Category add/edit admin panel
    """

    list_display = [
        'name',
        'name_fa',
        'name_ar',
        'slug'
    ]


@admin.register(VersionReviewVote)
class VersionReviewVoteAdmin(ReadOnlyAdmin):
    """
        VersionReviewVote view admin panel
    """

    list_display = [
        'review',
        'user',
        'vote',
    ]


class VersionReviewAdmin(ReadOnlyAdmin):
    """
        VersionReview view admin panel
    """

    list_display = [
        'tool_name',
        'platform_name',
        'tool_version',
        'rating',
        'text',
        'timestamp',
        'checked',
        'upvotes_count',
        'downvotes_count'
    ]

    search_fields = [
        'tool_name',
        'platform_name',
        'tool_version',
        'rating',
    ]

    ordering = ('-timestamp',)

    def __init__(self, *args, **kwargs):
        super(VersionReviewAdmin, self).__init__(*args, **kwargs)

        self.readonly_fields.remove('checked')
        self.readonly_fields.remove('category_ratings')
        self.readonly_fields.remove('votes')


class FeedbackAdmin(ReadOnlyAdmin):
    """
        Feedback view admin panel
    """

    list_display = [
        'status',
        'title',
        'text',
    ]

    search_fields = [
        'status',
        'title',
        'text'
    ]

    ordering = ('status', 'created')

    def __init__(self, *args, **kwargs):
        super(FeedbackAdmin, self).__init__(*args, **kwargs)

        self.readonly_fields.remove('status')


admin.site.register(VersionCategoryRating, VersionCategoryRatingAdmin)
admin.site.register(VersionReview, VersionReviewAdmin)
admin.site.register(Feedback, FeedbackAdmin)
