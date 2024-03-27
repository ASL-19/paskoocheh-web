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


class ToolVersionTutorialView(View, ToolVersionMixin):
    u"""View for tool version tutorial page."""

    @pk_cache_response()
    def get(self, request, **kwargs):
        u"""
        Generate a tool version tutorial page response.

        Get the tool version data and tool version tutorial matching the named
        group arguments, render the tool version tutorial page.

        Args:
            **platform_slug (string): tools.models.Version.slug
            **tool_id (string): tools.models.Tool.id
            **tutorial_id (string): tools.models.Tutorial.id

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
            tutorial = Tutorial.objects.get(
                id=self.kwargs['tutorial_id'],
                publishable=True,
                version=version_data.tool_version,
            )
        except Tutorial.DoesNotExist:
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'No tutorial matching this URL exists.',
                    )
                ),
            )

        view_metadata = PkViewMetadata(
            title=tutorial.title,
            description=False,
        )

        return render(
            self.request,
            'webfrontend/toolversiontutorial.html',
            context={
                'tutorial': tutorial,
                'version': version_data.tool_version,
                'version_name_localized': version_data.version_name_localized,
                'view_metadata': view_metadata,
            }
        )
