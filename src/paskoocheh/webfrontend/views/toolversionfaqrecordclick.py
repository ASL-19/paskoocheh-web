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
from django.views import View
from tools.models import Faq
from webfrontend.mixins import ToolVersionMixin
from webfrontend.utils.general import is_request_user_agent_noop

logger = logging.getLogger(__name__)


class ToolVersionFaqRecordClickView(View, ToolVersionMixin):
    u"""View for recording version FAQ clicks."""

    def post(self, request, **kwargs):
        u"""
        Increment tool version FAQ click_count.

        Args:
            **platform_slug (string): tools.models.Version.slug
            **tool_id (string): tools.models.Tool.id
            **faq_id (string): tools.models.Faq.id

        Returns:
            Empty HttpResponse with appropriate status code:
                204: Success
                404: FAQ not found
                500: Server error when calling faq.save()
        """
        if is_request_user_agent_noop(self.request):
            return HttpResponse(status=403)

        data_or_error_response = self.get_tool_version_data_or_error_response()

        if isinstance(data_or_error_response, HttpResponse):
            logger.error(
                u'Couldn’t record FAQ click because tool version with tool_id {tool_id} and supported_os__slug_name {supported_os__slug_name} doesn’t exist.'.format(
                    tool_id=self.kwargs['tool_id'],
                    supported_os__slug_name=self.kwargs['platform_slug'],
                )
            )
            return HttpResponse(status=404)
        else:
            data = data_or_error_response

        try:
            faq = Faq.objects.get(
                id=self.kwargs['faq_id'],
                publishable=True,
                version=data.tool_version,
            )
        except Faq.DoesNotExist as e:
            logger.exception(
                u'Couldn’t record FAQ click because FAQ with id {faq_id} and version_id {version_id} doesn’t exist: {error}'.format(
                    faq_id=self.kwargs['faq_id'],
                    version_id=data.tool_version.id,
                    error=str(e),
                )
            )
            return HttpResponse(status=404)

        faq.click_count += 1

        try:
            faq.save(update_fields=['click_count'])
        except Exception as e:
            logger.exception(
                u'Error when attempting to record click for tool version FAQ: {error}'.format(
                    error=str(e)
                )
            )
            return HttpResponse(status=500)

        return HttpResponse(status=204)
