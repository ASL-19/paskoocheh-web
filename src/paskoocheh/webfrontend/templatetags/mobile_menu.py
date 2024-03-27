# coding: utf-8
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

u"""Registers mobile_menu Django template tag."""

from django import template
from preferences.models import ToolType, Platform
from django.conf import settings
from django.utils.translation import pgettext
register = template.Library()

app = settings.PLATFORM


@register.inclusion_tag(
    'webfrontend/tags/mobile_menu.html',
    takes_context=True
)
def mobile_menu(context):
    u"""
    Build the context for the mobile_menu inclusion tag.

    Args:
        context (RequestContext) (injected by decorator)
        tool_types (List of ToolType)

    Returns:
        dictionary: Template context
    """
    tool_types = (
        ToolType.objects
        .exclude(
            name='Uncategorized tools'
        )
        .order_by('name')
    )

    # =========================================
    # === Read current filter search params ===
    # =========================================
    current_page_slug = None
    current_type_slug = None
    current_view_name = context['request'].resolver_match.url_name
    current_platform_slug = None

    query_string_args = context['request'].GET
    if 'category' in query_string_args:
        current_type_slug = query_string_args['category']

    if 'slug' in context['request'].resolver_match.kwargs:
        current_page_slug = context['request'].resolver_match.kwargs['slug']

    if 'platform' in query_string_args:
        current_platform_slug = query_string_args['platform']

    # ==========================
    # === Detect current app ===
    # ==========================

    app = settings.PLATFORM or None

    # ============================================
    # === Get localized global platform slug ===
    # ============================================

    global_platform = None
    if context['request'].global_platform_slug != 'all' and context['request'].global_platform_slug is not None:
        try:
            global_platform = Platform.objects.get(slug_name=context['request'].global_platform_slug)
        except Platform.DoesNotExist:
            from webfrontend.views import PageNotFoundView

            return PageNotFoundView.as_view()(
                context['request'],
                error_message=(
                    pgettext(
                        u'Error message',
                        u'URL contains unknown platform code “{platform_code}”.',
                    )
                    .format(
                        platform_code=context['request'].global_platform_slug,
                    )
                ),
            )

    localized_global_platform_name = None
    if global_platform is not None:
        localized_global_platform_name = global_platform.display_name_ar if app == 'zanga' else global_platform.display_name_fa

    # ============================================
    # === Get 3 lists of categorized platforms ===
    # ============================================

    platforms = (
        Platform.objects
        .all()
        .exclude(
            name__in=['linux32', 'windows32']
        )
        .order_by('slug_name')
    )

    desktop_platforms = None
    mobile_platforms = None
    web_platforms = None

    if platforms:
        desktop_platforms = [p for p in platforms if p.category == 'd']
        web_platforms = [p for p in platforms if p.category == 'w']
        mobile_platforms = [p for p in platforms if p.category == 'm']

        # Reverse the sorting of desktop platforms to show them as: Windows - Mac - Linux
        sorted_desktop_platforms = sorted(desktop_platforms, key=lambda platform: platform.slug_name, reverse=True)

        # Web platforms are already sorted based on the slug_name as: Chrome - Firefox
        # Mobile platforms are also sorted based on the slug_name as: Android - iOS - Windows Phone

    # ==================================
    # === Construct template context ===
    # ==================================
    return {
        'current_page_slug': current_page_slug,
        'current_type_slug': current_type_slug,
        'current_view_name': current_view_name,
        'current_platform_slug': current_platform_slug,
        'global_platform_slug': context['request'].global_platform_slug,
        'localized_global_platform_name': localized_global_platform_name,
        'tool_types': tool_types,
        'app': app,
        'sorted_desktop_platforms': sorted_desktop_platforms,
        'sorted_mobile_platforms': mobile_platforms,
        'sorted_web_platforms': web_platforms,
    }
