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
    GooglePlayApiPreference,
    PaskoochehAndroidPreference,
    PromoImage,
    Text,
    ToolType,
    Platform,
    GeneralPreference,
    Tag,
    AndroidDeviceProfile
)
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.utils.safestring import mark_safe


@admin.register(GeneralPreference, GooglePlayApiPreference, PaskoochehAndroidPreference)
class SingeltonSettingsAdmin(admin.ModelAdmin):
    """
        SingeltonSettings change admin panel
        A single row with multiple columns that can only be
        added/deleted from the command line
    """

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ToolType)
class ToolTypeAdmin(admin.ModelAdmin):
    """
        ToolType add/change admin panel
    """

    list_display = [
        'admin_thumbnail',
        'name',
    ]


@admin.register(PromoImage)
class PromoAdmin(admin.ModelAdmin):
    """
        Promo add/change admin panel
    """

    list_display = [
        'admin_thumbnail',
        'title',
        'link',
        'publish',
        'language',
        'order',
    ]

    list_display_links = [
        'admin_thumbnail',
        'title'
    ]

    ordering = (
        'language',
        'order',
    )


@admin.register(Text)
class TextAdmin(MarkdownxModelAdmin):
    """
        ToolType add/change admin panel
    """

    list_display = [
        'language',
        'publishable',
    ]

    ordering = (
        'language',
        'publishable',
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
        Tag add/change admin panel
    """

    list_display = [
        'name',
        'slug',
    ]


@admin.register(AndroidDeviceProfile)
class AndroidDeviceProfileAdmin(admin.ModelAdmin):
    """
        AndroidDeviceProfile add/change admin panel
    """

    list_display = [
        'name',
        'codename',
    ]

    list_filter = [
        'status',
    ]

    ordering = (
        'id',
    )

    # readonly_fields = ('properties_prettified',)

    @admin.display(
        description='Device Properties Prettified'
    )
    def properties_prettified(self, instance):
        """Function to display pretty version of device properties"""

        # Convert the data to sorted, indented JSON
        response = instance.properties

        # Truncate the data. Alter as needed
        response = response[:5000]

        # Get the Pygments formatter
        formatter = HtmlFormatter(style='colorful')

        # Highlight the data
        response = highlight(response, JsonLexer(), formatter)

        # Get the stylesheet
        style = '<style>' + formatter.get_style_defs() + '</style><br>'

        # Safe the output
        return mark_safe(style + response)


admin.site.register(Platform)
