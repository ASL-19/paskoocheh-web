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

u"""Registers main_header Django template tag."""

from django import template
from preferences.models import Platform, ToolType
from webfrontend.utils.uri import pask_reverse
from django.conf import settings
from django.db.models import Count
from django.utils.translation import pgettext

register = template.Library()

app = settings.PLATFORM


@register.inclusion_tag(
    'webfrontend/tags/main_header.html',
    takes_context=True
)
def main_header(context):
    u"""
    Build the context for the main_header inclusion tag.

    Args:
        context (RequestContext) (injected by decorator)

    Returns:
        dictionary: Template context
    """

    # ===========================================
    # === Read form values from search params ===
    # ===========================================
    hidden_form_values = {}
    request = context['request']
    search_query = ''

    # if 'category' in request.GET:
    #     hidden_form_values['category'] = request.GET['category']

    if 'query' in request.GET:
        search_query = request.GET['query']

    # ====================================
    # === Set destination of logo link ===
    # ====================================
    logo_link_destination = pask_reverse(
        'webfrontend:index',
        context.request,
        q_platform=request.global_platform_slug
    )

    nocookies = False
    if 'nocookies' in context.request.GET:
        nocookies = True

    # =============================
    # === Get list of platforms ===
    # =============================

    platforms = (
        Platform.objects
        .all()
        .exclude(
            name__in=['linux32', 'windows32']
        )
        .order_by('slug_name')
    )

    logo_path = f'webfrontend/images/{app}-logo.svg'

    tool_types = ToolType.objects.annotate(num_tools=Count('tools')).filter(num_tools__gt=0)

    # =========================================
    # === Read current filter search params ===
    # =========================================
    current_page_slug = None
    current_type_slug = None
    current_view_name = context['request'].resolver_match.url_name

    query_string_args = context['request'].GET
    if 'category' in query_string_args:
        current_type_slug = query_string_args['category']

    if 'slug' in context['request'].resolver_match.kwargs:
        current_page_slug = context['request'].resolver_match.kwargs['slug']

    global_platform = None
    if request.global_platform_slug != 'all' and request.global_platform_slug is not None:
        try:
            global_platform = Platform.objects.get(slug_name=request.global_platform_slug)
        except Platform.DoesNotExist:
            from webfrontend.views import PageNotFoundView

            return PageNotFoundView.as_view()(
                request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'URL contains unknown platform code “{platform_code}”.',
                    )
                    .format(
                        platform_code=request.global_platform_slug,
                    )
                ),
            )

    # ============================================
    # === Get localized global platform slug ===
    # ============================================

    localized_global_platform_name = None
    if global_platform is not None:
        localized_global_platform_name = global_platform.display_name_ar if app == 'zanga' else global_platform.display_name_fa

    # =========================================
    # === Get list of categorized platforms ===
    # =========================================

    desktop_platforms = None
    mobile_platforms = None
    web_platforms = None

    if platforms:
        desktop_platforms = [p for p in platforms if p.category == 'd']
        web_platforms = [p for p in platforms if p.category == 'w']
        mobile_platforms = [p for p in platforms if p.category == 'm']

        # Reverse the sorting of desktop platforms to show them as: Windows - Mac - Linux
        sorted_desktop_platforms = sorted(desktop_platforms, key=lambda platform: platform.slug_name, reverse=True)

        # Web platforms are already sorted by default as: Chrome - Firefox
        # Mobile platforms are also sorted by default as: Android - iOS - Windows Phone

    # ==================================
    # === Construct template context ===
    # ==================================
    return {
        'global_platform_slug': request.global_platform_slug,
        'localized_global_platform_name': localized_global_platform_name,
        'hidden_form_values': hidden_form_values,
        'logo_link_destination': logo_link_destination,
        'nocookies': nocookies,
        'search_query': search_query,
        'app': app,
        'logo_path': logo_path,
        'tool_types': tool_types,
        'current_page_slug': current_page_slug,
        'current_type_slug': current_type_slug,
        'current_view_name': current_view_name,
        'sorted_desktop_platforms': sorted_desktop_platforms,
        'sorted_web_platforms': web_platforms,
        'sorted_mobile_platforms': mobile_platforms,
    }
