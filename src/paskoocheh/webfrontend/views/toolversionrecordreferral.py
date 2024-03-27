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
import re
from django.http import HttpResponse
from django.views import View
from paskoocheh.helpers import get_client_ip
from stats.utils import save_download
from webfrontend import __version__ as webfrontend_version
from webfrontend.mixins import ToolVersionMixin
from webfrontend.utils.general import is_request_user_agent_noop

logger = logging.getLogger(__name__)


class ToolVersionRecordReferralView(View, ToolVersionMixin):
    u"""View for recording referrals to external tool sites
    (Version.download_url) as downloads."""

    def post(self, request, **kwargs):
        u"""
        Record download (via API) for the requested tool version.

        Args:
            **tool_id (string): tools.models.Tool.id
            **platform_slug (string): tools.models.Version.slug

        Returns:
            Empty HttpResponse with appropriate status code:
                204: Success
                404: Tool version not found
                500: Server error when calling save_download
        """
        if is_request_user_agent_noop(self.request):
            return HttpResponse(status=403)

        data_or_error_response = self.get_tool_version_data_or_error_response()

        if isinstance(data_or_error_response, HttpResponse):
            logger.error(
                u'Couldn’t record external download because tool version with tool_id {tool_id} and supported_os__slug_name {supported_os__slug_name} doesn’t exist.'.format(
                    tool_id=self.kwargs['tool_id'],
                    supported_os__slug_name=self.kwargs['platform_slug'],
                )
            )
            return HttpResponse(status=404)
        else:
            version_data = data_or_error_response

        downloaded_via = 'external-website'

        if (
            re.match(
                r'https?:\/\/appstore\.com\/.*',
                version_data.tool_version.download_url
            ) or
            re.match(
                r'https?:\/\/itunes\.apple\.com.*\/app\/.*',
                version_data.tool_version.download_url
            )
        ):
            downloaded_via = 'apple-app-store'
        elif (
            re.match(
                r'https?:\/\/chrome\.google\.com\/webstore\/.*',
                version_data.tool_version.download_url
            )
        ):
            downloaded_via = 'chrome-web-store'
        elif (
            re.match(
                r'https?:\/\/play\.google\.com\/store\/apps.*',
                version_data.tool_version.download_url
            )
        ):
            downloaded_via = 'google-play-store'
        elif (
            re.match(
                r'https?:\/\/(www\.)?microsoft\.com.*\/store.*',
                version_data.tool_version.download_url
            )
        ):
            downloaded_via = 'microsoft-store'
        elif (
            re.match(
                r'https?:\/\/addons\.mozilla\.org.*\/firefox\/addon\/.*',
                version_data.tool_version.download_url
            )
        ):
            downloaded_via = 'mozilla-addons-directory'

        try:
            request_ip = get_client_ip(self.request)

            save_download(
                channel_version=webfrontend_version,
                downloaded_via=downloaded_via,
                request_ip=(request_ip).encode('utf-8'),
                version_id=version_data.tool_version.id,
            )
        except Exception as e:
            logger.exception(u'Error when attempting to record download: {error}'.format(
                error=str(e)
            ))
            return HttpResponse(status=500)

        return HttpResponse(status=204)
