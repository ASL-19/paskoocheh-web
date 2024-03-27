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

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import pgettext
from django.views import View
from tools.models import Tutorial
from webfrontend.caches.responses.decorators import pk_cache_response
from webfrontend.mixins import ToolVersionMixin
from webfrontend.templatetags.pk_meta_tags import PkViewMetadata
from webfrontend.utils.general import wrap_with_link
from webfrontend.utils.query import add_select_related_to_tutorials_queryset
from webfrontend.utils.uri import pask_reverse


class ToolVersionTutorialsView(View, ToolVersionMixin):
    u"""View for tool version tutorials page."""

    @pk_cache_response()
    def get(self, request, **kwargs):
        u"""
        Generate a tool version tutorials page response.

        Get the tool version data and tool version tutorials matching the named
        group arguments, render the tool version tutorials page.

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

        tutorials = add_select_related_to_tutorials_queryset(
            Tutorial.objects
            .filter(
                language=self.request.LANGUAGE_CODE,
                publishable=True,
                version=version_data.tool_version,
            )
            .order_by('order')
        )

        if tutorials.count() == 0:
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'No tutorials found for {tool_name_and_platform}.',
                    )
                    .format(
                        tool_name_and_platform=version_data.version_name_localized,
                    )
                ),
                status=200,
                status_string=(
                    pgettext(
                        u'Error title',
                        u'No tutorials found',
                    )
                ),
            )

        page_heading_inner_html = (
            pgettext(
                u'Tutorial',
                # Translators: Title of tool version tutorials listing
                u'Tutorials for {tool_name_and_version}',
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
                u'Tutorial',
                u'Tutorials for {tool_name_and_version}',
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
            'webfrontend/toolversiontutorials.html',
            context={
                'page_heading_inner_html': page_heading_inner_html,
                'page_title': page_title,
                'tutorials': tutorials,
                'version': version_data.tool_version,
                'view_metadata': view_metadata,
            }
        )
