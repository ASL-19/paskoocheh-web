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

from django.shortcuts import redirect, render
from django.utils.translation import pgettext
from django.views import View
from operator import attrgetter
from preferences.models import Platform, PromoImage, ToolType
from tools.models import Tool, Version
from blog.models import Post
from urllib.parse import urlencode
from webfrontend.templatetags.pk_meta_tags import PkViewMetadata
from webfrontend.templatetags.tool_list import (
    construct_tool_list_item_context_list,
)
from webfrontend.caches.responses.decorators import pk_cache_response
from webfrontend.utils.query import (
    add_prefetch_related_to_tools_queryset,
    get_filter_platform_slugs,
)
from webfrontend.utils.tool_list import get_tool_list_title
from webfrontend.utils.uri import pask_reverse
from webfrontend.utils.blog import get_blog_post_list_title
from django.conf import settings

app = settings.PLATFORM


class IndexView(View):
    u"""View for index page (/)."""

    @pk_cache_response()
    def get(self, request, *args, **kwargs):        # noqa C901
        u"""Get all tools and render the homepage.

        Returns:
            HttpResponse: Rendered page
        """

        # =================================
        # === Rerouting and redirection ===
        # =================================

        # Legacy URL handling: if request has opensource or query param,
        # immediately dispatch request to SearchView:
        if (set(['opensource', 'query']).intersection(request.GET)):
            query_string_args = {}

            if (
                'opensource' in request.GET and
                request.GET['opensource'] in ['', 'true']
            ):
                query_string_args['opensource'] = 'true'

            if 'query' in request.GET:
                query_string_args['query'] = request.GET['query']

            return redirect(
                pask_reverse(
                    'webfrontend:search',
                    request
                ) + '?' + urlencode(query_string_args),
                permanent=True,
            )

        platform_slug = None

        # If global_platform cookie is set but URL has ?platform, redirect to
        # /?platform={{ global_platform }}
        if 'platform' in request.GET:
            platform_slug = request.GET['platform']

            if platform_slug == 'osx':
                return redirect(
                    pask_reverse(
                        'webfrontend:index',
                        request,
                        q_platform='macos',
                    ),
                    permanent=True,
                )
        else:
            return redirect(
                pask_reverse(
                    'webfrontend:index',
                    request,
                    q_platform=request.global_platform_slug
                )
            )

        # =====================================
        # === Get platform and/or tool type ===
        # =====================================

        # Now that we know the request doesn’t require a redirect or reroute,
        # move on to core index view logic.

        filter_args = {
            'versions__isnull': False
        }

        # === Platform (supported OS) ===
        platform = None

        if platform_slug != 'all':
            try:
                platform = Platform.objects.get(slug_name=platform_slug)
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
                            platform_code=platform_slug,
                        )
                    ),
                )

            filter_args['versions__supported_os__slug_name__in'] = (
                get_filter_platform_slugs(platform.slug_name)
            )

        # === Category (tool type) ===
        tool_type = None
        type_slug = None

        if 'category' in request.GET:
            type_slug = request.GET['category']

            try:
                tool_type = ToolType.objects.get(slug=type_slug)
                filter_args['tooltype'] = tool_type
            except ToolType.DoesNotExist:
                from webfrontend.views import PageNotFoundView

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

        # ========================
        # === Build tool lists ===
        # ========================
        # Build tool lists and get SearchView paths for each

        base_search_reverse_args = {
            'q_platform': platform_slug,
        }
        if tool_type is not None:
            base_search_reverse_args['q_category'] = type_slug

        platform_locale_display_name = None
        tool_type_name = None

        if platform:
            platform_locale_display_name = platform.display_name_ar if app == 'zanga' else platform.display_name_fa

        if tool_type:
            tool_type_name = tool_type.name_ar if app == 'zanga' else tool_type.name_fa

        base_title_args = {
            'platform_locale_display_name': platform_locale_display_name,
            'tool_type_name': tool_type_name
        }

        page_title = get_tool_list_title(**base_title_args)

        # === All matched tools ===
        # Used as a basis for other lists since it’s a superset of all possible
        # lists. Also displayed in lieu of other lists if there are 7 or fewer
        # tools.
        all_matched_tools = add_prefetch_related_to_tools_queryset(
            Tool.objects.filter(**filter_args).distinct('name'),
            request,
            platform.slug_name if platform else None,
        )

        all_matched_search_path = pask_reverse(
            'webfrontend:search',
            request,
            **base_search_reverse_args
        )

        all_matched_title = get_tool_list_title(**base_title_args)

        all_matched_tools_list_item_contexts = (
            construct_tool_list_item_context_list(
                request=request,
                stats_for_platform_slug_name=platform_slug,
                tools=all_matched_tools,
            )
        )

        show_sorted_lists = (len(all_matched_tools_list_item_contexts) >= 7)

        # === Other lists ===
        # Don’t bother generating other lists if they won’t be displayed
        if show_sorted_lists:
            # Just added tools
            just_added_search_path = pask_reverse(
                'webfrontend:search',
                request,
                q_orderby='dateadded',
                **base_search_reverse_args
            )

            just_added_title = get_tool_list_title(
                order_by_slug='dateadded',
                **base_title_args
            )

            just_added_tools_list_item_contexts = sorted(
                all_matched_tools_list_item_contexts,
                key=attrgetter('version.last_modified'),
                reverse=True
            )[:7]

            # Most downloaded tools
            most_downloaded_search_path = pask_reverse(
                'webfrontend:search',
                request,
                q_orderby='downloadcount',
                **base_search_reverse_args
            )

            most_downloaded_title = get_tool_list_title(
                order_by_slug='downloadcount',
                requires_article_prefix=(app == 'zanga'),
                **base_title_args
            )

            most_downloaded_tools_list_item_contexts = sorted(
                all_matched_tools_list_item_contexts,
                key=attrgetter('download_count'),
                reverse=True
            )[:7]

            # Recently updated tools
            recently_updated_search_path = pask_reverse(
                'webfrontend:search',
                request,
                q_orderby='dateupdated',
                **base_search_reverse_args
            )

            recently_updated_title = get_tool_list_title(
                order_by_slug='dateupdated',
                **base_title_args
            )

            recently_updated_tools_list_item_contexts = sorted(
                all_matched_tools_list_item_contexts,
                key=attrgetter('version.release_date'),
                reverse=True
            )[:7]
        else:
            just_added_search_path = None
            just_added_title = None
            just_added_tools_list_item_contexts = None
            most_downloaded_search_path = None
            most_downloaded_title = None
            most_downloaded_tools_list_item_contexts = None
            recently_updated_search_path = None
            recently_updated_title = None
            recently_updated_tools_list_item_contexts = None

        # ========================
        # === Get promo images ===
        # ========================

        promo_images = None

        if not tool_type:
            promo_images = (
                PromoImage.objects
                .filter(
                    language=self.request.LANGUAGE_CODE,
                    publish=True,
                )
                .order_by('order')
            )

        # ================
        # === Metadata ===
        # ================

        view_metadata = PkViewMetadata(
            title=page_title,
            description=None,
        )

        # ==========================
        # === Browser extensions ===
        # ==========================

        browser_extensions = None

        if not tool_type:
            browser_extensions = (
                Version.objects
                .filter(
                    supported_os__slug_name__in=['firefox', 'chrome'],
                )
                .order_by('created')[:6]
            )

        # ====================
        # === Latest posts ===
        # ====================

        latest_posts = None

        if not tool_type:
            latest_posts = (
                Post.objects
                .filter(
                    language=self.request.LANGUAGE_CODE,
                    status='p'
                )
                .order_by('-published_date')[:3]
            )

        latest_posts_title = get_blog_post_list_title()

        # This variable is used to have different padding/spacing
        # for the main container on the same view
        is_carousel_visible = 'category' not in self.request.GET

        return render(
            request,
            'webfrontend/index.html',
            context={
                'all_matched_search_path': all_matched_search_path,
                'all_matched_title': all_matched_title,
                'all_matched_tools_list_item_contexts': all_matched_tools_list_item_contexts,
                'just_added_search_path': just_added_search_path,
                'just_added_title': just_added_title,
                'just_added_tools_list_item_contexts': just_added_tools_list_item_contexts,
                'most_downloaded_search_path': most_downloaded_search_path,
                'most_downloaded_title': most_downloaded_title,
                'most_downloaded_tools_list_item_contexts': most_downloaded_tools_list_item_contexts,
                'recently_updated_search_path': recently_updated_search_path,
                'recently_updated_title': recently_updated_title,
                'recently_updated_tools_list_item_contexts': recently_updated_tools_list_item_contexts,
                'page_title': page_title,
                'promo_images': promo_images,
                'show_sorted_lists': show_sorted_lists,
                'view_metadata': view_metadata,
                'is_carousel_visible': is_carousel_visible,
                'browser_extensions': browser_extensions,
                'latest_posts': latest_posts,
                'latest_posts_title': latest_posts_title,
            }
        )
