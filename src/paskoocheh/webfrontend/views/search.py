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

from copy import deepcopy
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.translation import pgettext
from django.views import View
from preferences.models import Platform, ToolType
from tools.models import Tool
from webfrontend.caches.responses.decorators import pk_cache_response
from webfrontend.templatetags.pk_meta_tags import PkViewMetadata
from webfrontend.templatetags.tool_list import (
    construct_tool_list_item_context_list,
)
from webfrontend.utils.query import (
    add_prefetch_related_to_tools_queryset,
    get_filter_platform_slugs,
)
from webfrontend.utils.tool_list import get_tool_list_title
from webfrontend.utils.uri import (
    get_prefixed_query_string_args,
    pask_reverse,
)
from django.conf import settings

app = settings.PLATFORM


class SearchView(View):
    u"""View for search page (/?)."""

    def get_base_tool_search_queryset(self, filter_args, search_query):
        u"""
        Returns a queryset for searching with a search query. Queries on both
        the name and infos.name (localized name), and excludes duplicates.

        TODO: Handle different combinations of `language` once localization is
        set up.

        Returns:
            search_queryset (QuerySet)
        """
        search_queryset = (
            Tool.objects
            .filter(
                (
                    Q(name__icontains=search_query) |
                    (
                        Q(infos__name__icontains=search_query) &
                        (
                            Q(infos__language=self.request.LANGUAGE_CODE) |
                            Q(infos__language='en')
                        )
                    )
                ) &
                Q(**filter_args)
            )
        )

        return search_queryset

    @pk_cache_response()
    def get(self, request, *args, **kwargs):        # noqa: C901
        u"""Query requested tools and render the homepage (placeholder).

        Returns:
            HttpResponse: Rendered page
        """
        from webfrontend.views import PageNotFoundView

        # Override the request’s view name since all search view requests begin
        # as index view requests before being rerouted
        request.resolver_match.url_name = 'search'

        # ===========================================================
        # === Make sure required platform query string arg exists ===
        # ===========================================================

        if 'platform' not in request.GET:
            prefixed_query_string_args = get_prefixed_query_string_args(request.GET)
            prefixed_query_string_args['q_platform'] = request.global_platform_slug

            redirect_path = (
                pask_reverse(
                    'webfrontend:search',
                    request,
                    **prefixed_query_string_args
                )
            )

            return redirect(redirect_path)

        # =======================================
        # === Populate query filter arguments ===
        # =======================================

        filter_args = {
            'versions__isnull': False
        }
        get_platform_slug = request.GET['platform']
        platform = None

        # === Platform ===
        if get_platform_slug != 'all':
            if get_platform_slug == 'osx':
                prefixed_query_string_args = get_prefixed_query_string_args(request.GET)
                prefixed_query_string_args['q_platform'] = 'macos'

                return redirect(
                    pask_reverse(
                        'webfrontend:search',
                        request,
                        **prefixed_query_string_args
                    ),
                    permanent=True,
                )

            try:
                platform = Platform.objects.get(slug_name=get_platform_slug)
            except Platform.DoesNotExist:
                return PageNotFoundView.as_view()(
                    request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            u'URL contains unknown platform code “{platform_code}”.',
                        )
                        .format(
                            platform_code=get_platform_slug,
                        )
                    ),
                )

            filter_args['versions__supported_os__slug_name__in'] = (
                get_filter_platform_slugs(platform.slug_name)
            )

        # === Category (tool type) ===
        if 'category' in request.GET:
            type_slug = request.GET['category']

            try:
                filter_args['tooltype'] = ToolType.objects.get(slug=type_slug)
            except ToolType.DoesNotExist:
                return PageNotFoundView.as_view()(
                    request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            u'URL contains unknown category code “{category_code}“.',
                        )
                        .format(
                            category_code=type_slug,
                        )
                    ),
                )

        # === Featured ===
        if 'featured' in request.GET:
            if request.GET['featured'] == 'true':
                filter_args['featured'] = True
            else:
                return PageNotFoundView.as_view()(
                    request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            u'URL contains invalid featured value.',
                        )
                    ),
                    status=400,
                )

        order_by = None
        order_reverse = False
        order_by_slug = None

        if 'orderby' in request.GET:
            if request.GET['orderby'] == 'downloadcount':
                order_by = 'download_count'
                order_reverse = True
                order_by_slug = 'downloadcount'
            elif request.GET['orderby'] == 'dateadded':
                order_by = 'version.id'
                order_reverse = True
                order_by_slug = 'dateadded'
            elif request.GET['orderby'] == 'dateupdated':
                order_by = 'version.release_date'
                order_reverse = True
                order_by_slug = 'dateupdated'
            else:
                return PageNotFoundView.as_view()(
                    request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            u'URL contains invalid orderby value.',
                        )
                    ),
                    status=400,
                )

        # === Query (search) ===
        other_platform_tools_list_item_contexts = None
        search_query = None

        if 'query' in request.GET:
            search_query = request.GET['query']

            if search_query == '':
                return PageNotFoundView.as_view()(
                    request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            u'Search query cannot be empty.',
                        )
                    ),
                    status=400,
                )

            filtered_tools = (
                add_prefetch_related_to_tools_queryset(
                    (
                        self.get_base_tool_search_queryset(
                            filter_args,
                            search_query
                        )
                    ),
                    request,
                    platform.slug_name if platform else None,
                ).distinct('name')
            )
        else:
            filtered_tools = (
                add_prefetch_related_to_tools_queryset(
                    Tool.objects.filter(**filter_args),
                    request,
                    platform.slug_name if platform else None,
                )
            ).distinct('name')

        filtered_tools_list_item_contexts = (
            construct_tool_list_item_context_list(
                order_by=order_by,
                order_reverse=order_reverse,
                request=request,
                stats_for_platform_slug_name=get_platform_slug,
                tools=filtered_tools,
            )
        )

        if platform:
            other_platform_filter_args = deepcopy(filter_args)
            other_platform_filter_args.pop('versions__supported_os__slug_name__in', None)

            if 'query' in request.GET:
                # If search has a query, we perform the same search for tools
                # that DO NOT support the platform (that is, excluding tools
                # that DO support the requested platform) to be shown after the
                # main results
                other_platform_tools = (
                    add_prefetch_related_to_tools_queryset(
                        (
                            self.get_base_tool_search_queryset(
                                other_platform_filter_args,
                                search_query
                            )
                            .exclude(
                                versions__supported_os__slug_name__in=(
                                    get_filter_platform_slugs(platform.slug_name)
                                )
                            )
                        ),
                        request
                    )
                ).distinct('name')
            else:
                other_platform_tools = (
                    add_prefetch_related_to_tools_queryset(
                        (
                            Tool.objects.filter(**other_platform_filter_args)
                            .exclude(
                                versions__supported_os__slug_name__in=(
                                    get_filter_platform_slugs(platform.slug_name)
                                )
                            )
                        ),
                        request
                    )
                ).distinct('name')

            other_platform_tools_list_item_contexts = (
                construct_tool_list_item_context_list(
                    order_by=order_by,
                    order_reverse=order_reverse,
                    request=request,
                    stats_for_platform_slug_name='all',
                    tools=other_platform_tools,
                )
            )

        # =====================================
        # === Get tool_list_title arguments ===
        # =====================================

        platform_locale_display_name = None
        tool_type_name = None

        if platform:
            platform_locale_display_name = platform.display_name_ar if app == 'zanga' else platform.display_name_fa

        if 'tooltype' in filter_args:
            tool_type_name = filter_args['tooltype'].name_ar if app == 'zanga' else filter_args['tooltype'].name_fa

        filtered_tools_title = get_tool_list_title(
            is_featured='featured' in filter_args,
            order_by_slug=order_by_slug,
            platform_locale_display_name=platform_locale_display_name,
            query=search_query,
            tool_type_name=tool_type_name,
            requires_article_prefix=(order_by_slug == 'downloadcount' and app == 'zanga'),
        )

        other_platform_tools_title = get_tool_list_title(
            is_featured='featured' in filter_args,
            is_for_other_platforms=True,
            order_by_slug=order_by_slug,
            platform_locale_display_name=platform_locale_display_name,
            query=search_query,
            tool_type_name=tool_type_name,
            requires_article_prefix=(app == 'zanga'),
        )

        view_metadata = PkViewMetadata(
            title=filtered_tools_title
        )

        return render(
            request,
            'webfrontend/search.html',
            context={
                'filtered_tools_list_item_contexts': filtered_tools_list_item_contexts,
                'filtered_tools_title': filtered_tools_title,
                'other_platform_tools_list_item_contexts': other_platform_tools_list_item_contexts,
                'other_platform_tools_title': other_platform_tools_title,
                'view_metadata': view_metadata,
            }
        )
