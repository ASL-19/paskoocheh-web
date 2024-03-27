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

from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models.functions import Length
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import pgettext
from django.views import View
from stats.models import VersionReview
from webfrontend.caches.responses.decorators import pk_cache_response
from webfrontend.mixins import ToolVersionMixin
from webfrontend.templatetags.pk_meta_tags import PkViewMetadata
from webfrontend.utils.general import wrap_with_link
from webfrontend.utils.uri import pask_reverse

REVIEWS_PER_PAGE = 10


class ToolVersionReviewsView(View, ToolVersionMixin):
    u"""View for tool version reviews page."""

    @pk_cache_response()
    def get(self, request, **kwargs):
        u"""
        Generate a tool version reviews page response.

        Get the tool version data and tool version reviews matching the named
        group arguments, render the tool version reviews page.

        Args:
            **platform_slug (string): tools.models.Version.slug
            **tool_id (string): tools.models.Tool.id

        Returns:
            HttpResponse
        """
        from webfrontend.views import PageNotFoundView

        data_or_error_response = self.get_tool_version_data_or_error_response()

        if isinstance(data_or_error_response, HttpResponse):
            return data_or_error_response
        else:
            version_data = data_or_error_response

        tool_version_reviews = (
            VersionReview.objects
            .annotate(
                text_len=Length('text')
            )
            .filter(
                language=request.LANGUAGE_CODE,
                platform_name=version_data.tool_version.supported_os.slug_name,
                text_len__gte=3,
                tool_name=version_data.tool_version.tool.name,
            )
            .order_by('-timestamp')
        )

        reviews_paginator = Paginator(tool_version_reviews, REVIEWS_PER_PAGE)

        page_arg = self.request.GET.get('page', None)

        if page_arg == '1':
            return redirect(
                pask_reverse(
                    'webfrontend:toolversionreviews',
                    self.request,
                    p_tool_id=version_data.tool.id,
                    p_platform_slug=version_data.tool_version.supported_os.slug_name
                ),
                permanent=True
            )

        try:
            page = int(page_arg) if page_arg is not None else 1
            if page < 1:
                raise ValueError()

            current_page_reviews = reviews_paginator.page(page)
        except EmptyPage:
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        # Translators: Shown if a review URL contains a “page”
                        # parameter that causes no reviews to be returned.
                        u'There are no reviews on this page.',
                    )
                    .format(
                        page_arg=page_arg
                    )
                )
            )
        except (InvalidPage, ValueError):
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        # Translators: Shown if a user manually enters a URL
                        # with an invalid “page” parameter (e.g. not a number,
                        # less than 1, etc.)
                        u'URL contains invalid page value “{page_arg}”.',
                    )
                    .format(
                        page_arg=page_arg
                    )
                )
            )

        for review in current_page_reviews:
            review.url_path = pask_reverse(
                'webfrontend:toolversionreview',
                self.request,
                p_tool_id=version_data.tool_version.tool.id,
                p_platform_slug=version_data.tool_version.supported_os.slug_name,
                p_review_id=review.id
            )

        page_heading_inner_html = (
            pgettext(
                u'Review',
                # Translators: Title of tool version reviews listing
                u'Reviews for {tool_name_and_version}',
            )
            .format(
                tool_name_and_version=wrap_with_link(
                    version_data.version_name_localized,
                    pask_reverse(
                        'webfrontend:toolversion',
                        self.request,
                        p_tool_id=version_data.tool.id,
                        p_platform_slug=version_data.tool_version.supported_os.slug_name,
                    )
                )
            )
        )

        page_title = (
            pgettext(
                u'Review',
                u'Reviews for {tool_name_and_version}',
            )
            .format(
                tool_name_and_version=version_data.version_name_localized
            )
        )

        view_metadata = PkViewMetadata(
            title=page_title,
        )

        return render(
            self.request,
            'webfrontend/toolversionreviews.html',
            context={
                'current_page_reviews': current_page_reviews,
                'page_heading_inner_html': page_heading_inner_html,
                'page_title': page_title,
                'version': version_data.tool_version,
                'version_name_localized': version_data.version_name_localized,
                'view_metadata': view_metadata,
            }
        )
