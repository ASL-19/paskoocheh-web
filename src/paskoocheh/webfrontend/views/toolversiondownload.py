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

import logging
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import pgettext
from django.views import View
from paskoocheh.helpers import get_client_ip
from stats.utils import save_download
from webfrontend import __version__ as webfrontend_version
from webfrontend.mixins import ToolVersionMixin
from webfrontend.utils.general import is_request_user_agent_noop, get_temp_s3_url
from webfrontend.views import PageNotFoundView

logger = logging.getLogger(__name__)


class ToolVersionDownloadView(View, ToolVersionMixin):
    u"""View for tool version download redirects."""

    def get(self, request, **kwargs):
        u"""
        Get the appropriate download link for a tool version and return an HTTP
        redirect to it. If the tool version can’t be found or the requested S3
        URL is blank, returns a PageNotFoundView.

        Args:
            **platform_slug (string): tools.models.Version.slug
            **tool_id (string): tools.models.Tool.id

        Returns:
            HttpResponse
        """
        if is_request_user_agent_noop(self.request):
            return HttpResponse(status=403)

        data_or_error_response = self.get_tool_version_data_or_error_response(
            linux32_allowed=True,
            windows32_allowed=True
        )

        if isinstance(data_or_error_response, HttpResponse):
            # Return the PageNotFoundView
            return data_or_error_response
        else:
            data = data_or_error_response

        # Get temporary S3 download link
        tool_version_s3_temp_url = get_temp_s3_url(data.tool_version)
        if tool_version_s3_temp_url == '':
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'Sorry, the server wasn’t able to find a file for {tool_name}. If this doesn’t seem right, please contact contact us.',
                    )
                    .format(
                        tool_name=data.version_name_localized,
                    )
                ),
                status=500,
            )

        try:
            request_ip = get_client_ip(self.request)

            save_download(
                channel_version=webfrontend_version,
                downloaded_via='s3',
                request_ip=(request_ip).encode('utf-8'),
                version_id=data.tool_version.id,
            )
        except Exception as e:
            logger.exception(u'Error when attempting to record download: {error}'.format(
                error=str(e)
            ))

        return redirect(
            tool_version_s3_temp_url,
            permanent=False
        )
