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
from django.contrib.contenttypes.admin import GenericTabularInline
from markdownx.admin import MarkdownxModelAdmin
from tools.models import (
    Faq,
    Info,
    # Report,
    Tool,
    HomeFeaturedTool,
    Image,
    Tutorial,
    Guide,
    Version,
    AndroidSplitFile,
    VersionCode,
    TeamAnalysis,
    CategoryAnalysis
)


class ImageInline(GenericTabularInline):
    """
        Whenever a tool info is updated we would like to send a notification to all the
        users who had downloaded the previous versions
    """

    change_form_template = 'admin/tools/change_form_original.html'
    model = Image
    extra = 1

    readonly_fields = (
        'get_thumbnail_admin_list_display',
    )


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    """
        Whenever a tool is updated we would like to send a notification to all the users
        who had downloaded the previous versions
    """

    change_form_template = 'admin/tools/change_form_original.html'
    search_fields = [
        'name',
        'tooltype__name']
    inlines = [
        ImageInline,
    ]
    list_display = (
        'name',
        'id',
        'primary_tooltype',
        'featured',
        'last_modified',
        'publishable',
    )
    list_filter = (
        'primary_tooltype',
    )
    ordering = (
        'name',
    )

    # Automatically generate the value for slug
    prepopulated_fields = {'slug': ('name',)}


@admin.register(HomeFeaturedTool)
class HomeFeaturedToolAdmin(admin.ModelAdmin):
    """
        A single row with multiple columns that can only be
        added/deleted from the command line
    """

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AndroidSplitFileAdmin(admin.StackedInline):
    model = AndroidSplitFile
    extra = 0
    readonly_fields = (
        's3_key',
        'size',
    )
    fields = (
        'split_file',
        'devices',
        's3_key',
        'size',
    )


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    """
        Whenever a version is updated we would like to send a notification to all the users
        who had downloaded the previous versions
    """

    change_form_template = 'admin/tools/change_form.html'
    search_fields = [
        'tool__name',
        'supported_os__display_name',
        'version_number']
    list_display = (
        'get_tool_name',
        'get_tool_id',
        'get_supported_os_name',
        'version_number',
        'delivery_email',
        'last_modified',
        'publishable')
    readonly_fields = (
        'last_modified',
        'created',
        'release_jdate',
        'delivery_email',
        'faq_url',
        'guide_url',
        'is_bundled_app'
    )
    fields = (
        'tool',
        'version_number',
        'supported_os',
        'release_date',
        'release_jdate',
        'last_modified',
        'created',
        'download_url',
        'release_url',
        'delivery_email',
        'package_name',
        'auto_update',
        'is_bundled_app',
        'permissions',
        'faq_url',
        'guide_url',
        'video',
        'video_link',
        'publishable'
    )

    ordering = (
        'tool__name',
        'supported_os__display_name',
    )

    inlines = [
        ImageInline,
        # AndroidSplitFileAdmin,
    ]


@admin.register(VersionCode)
class VersionCodeAdmin(admin.ModelAdmin):
    model = VersionCode
    inlines = [AndroidSplitFileAdmin]
    list_display = (
        '__str__',
        'get_platform_name'
    )


class AndroidSplitFileAdmin(admin.ModelAdmin):
    pass


@admin.register(Guide)
class GuideAdmin(MarkdownxModelAdmin):
    """
        Guide add/change panel for admin
    """

    change_form_template = 'admin/tools/change_form_original.html'
    search_fields = [
        'version__tool__name',
        'headline']
    list_display = (
        'headline',
        'get_version_name',
        'language',
        'order',
        'publishable',
    )
    ordering = (
        'version__tool__name',
        'language',
        'order',
    )


@admin.register(Faq)
class FaqAdmin(MarkdownxModelAdmin):
    """
        Faq add/change panel for admin
    """

    change_form_template = 'admin/tools/change_form_original.html'
    search_fields = [
        'tool__name',
        'headline']
    list_display = (
        'headline',
        'get_version_name',
        'get_tool_name',
        'language',
        'order',
        'publishable',
    )
    ordering = (
        'tool__name',
        'version',
        'language',
        'order',
    )


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    """
        Tutorial add/change panel for admin
    """

    change_form_template = 'admin/tools/change_form_original.html'
    search_fields = ['title', 'version__tool__name']
    list_display = (
        'title',
        'get_version_name',
        'language',
        'order',
        'publishable',
    )

    ordering = (
        'version__tool__name',
        'language',
        'order',
    )


@admin.register(Info)
class InfoAdmin(MarkdownxModelAdmin):
    """
        Info add/change panel for admin
    """

    change_form_template = 'admin/tools/change_form_original.html'
    search_fields = ['tool__name']
    list_display = (
        'name',
        'get_tool_name',
        'language',
        'publishable',
    )
    ordering = (
        'tool__name',
        'language',
    )


class CategoryAnalysisAdmin(admin.TabularInline):
    """
        Category Analysis inline panel in TeamAnalysis admin page
    """

    model = CategoryAnalysis
    fieldsets = [
        (None, {
            'fields': ('rating_category', 'rating', ),
        }),
    ]
    extra = 1


@admin.register(TeamAnalysis)
class TeamAnalysis(admin.ModelAdmin):
    """
        Team Analysis add/change panel for admin
    """

    change_form_template = 'admin/tools/change_form_original.html'
    inlines = [
        CategoryAnalysisAdmin,
    ]


# admin.site.register(Report)
