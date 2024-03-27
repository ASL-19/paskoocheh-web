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

from django.db.models.functions import Length
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import pgettext
from django.views import View
from stats.models import VersionReview
from webfrontend.caches.responses.decorators import pk_cache_response
from webfrontend.mixins import ToolVersionMixin
from webfrontend.templatetags.pk_meta_tags import PkViewMetadata
from webfrontend.utils.general import wrap_with_link
from webfrontend.utils.uri import pask_reverse


class ToolVersionReviewView(View, ToolVersionMixin):
    u"""View for tool version review page."""

    @pk_cache_response()
    def get(self, request, **kwargs):
        u"""
        Generate a tool version review page response.

        Get the tool version data and tool version review matching the named
        group arguments, render the tool version review page.

        Args:
            **platform_slug (string): tools.models.Version.slug
            **tool_id (string): tools.models.Tool.id
            **review_id (string): stats.models.VersionReview.id

        Returns:
            HttpResponse
        """
        from webfrontend.views import PageNotFoundView

        data_or_error_response = self.get_tool_version_data_or_error_response()

        if isinstance(data_or_error_response, HttpResponse):
            return data_or_error_response
        else:
            version_data = data_or_error_response

        try:
            review = (
                VersionReview.objects
                .annotate(
                    text_len=Length('text')
                )
                .get(
                    id=self.kwargs['review_id'],
                    platform_name=version_data.tool_version.supported_os.slug_name,
                    text_len__gte=3,
                    tool_name=version_data.tool_version.tool.name,
                )
            )
        except VersionReview.DoesNotExist:
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'No review matching this URL exists.',
                    )
                ),
            )

        review_h1_inner_html = (
            pgettext(
                u'Review',
                # Translators: Single review title
                u'Review for {tool_name_and_version}',
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
                u'Review for {tool_name_and_version}'
            )
            .format(
                tool_name_and_version=version_data.version_name_localized
            )
        )

        view_metadata = PkViewMetadata(
            title=page_title,
            description=(review.text or False),
        )

        return render(
            self.request,
            'webfrontend/toolversionreview.html',
            context={
                'page_title': page_title,
                'review': review,
                'review_h1_inner_html': review_h1_inner_html,
                'version_name_localized': version_data.version_name_localized,
                'version': version_data.tool_version,
                'view_metadata': view_metadata,
            }
        )
