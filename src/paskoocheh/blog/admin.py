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
from markdownx.admin import MarkdownxModelAdmin
from .models import (
    Category,
    Post,
    Comment,
)


@admin.register(Post)
class PostAdmin(MarkdownxModelAdmin):
    """
        Post add/change panel
    """
    readonly_fields = (
        'get_post_link_admin_display',
        'published_date',
    )
    fields = (
        'title',
        'published_date',
        'status',
        'slug',
        'get_post_link_admin_display',
        'language',
        'author',
        'homepage_feature',
        'feature_image',
        'feature_image_caption',
        'category',
        'tags',
        'tool_tag',
        'version_tag',
        'content',
        'summary',
        'video',
    )
    list_display = (
        'title',
        'language',
        'category',
        'status',
        'get_tags_admin_list_display',
        'get_tool_tags_admin_list_display',
        'get_version_tags_admin_list_display',
        'homepage_feature',
        'published_date',
    )
    ordering = ('-published_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
        Comment change panel
    """

    list_display = (
        'approved',
        'name',
        'title'
    )

    def has_add_permission(self, request):
        """
            Remove the ability to add to comments for admin
        """

        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
        Category add/change panel
    """

    list_display = (
        'name',
        'name_fa',
        'name_ar',
        'slug',
    )
    ordering = ('name',)
