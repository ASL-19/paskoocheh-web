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
from tools.models import Faq, Tool
from webfrontend.utils.general import is_request_user_agent_noop

logger = logging.getLogger(__name__)


class ToolFaqRecordClickView(View):
    u"""View for recording tool FAQ clicks."""

    def post(self, request, **kwargs):
        u"""
        Increment tool FAQ click_count.

        Args:
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

        try:
            tool = Tool.objects.get(
                id=self.kwargs['tool_id'],
            )
        except Tool.DoesNotExist as e:
            logger.exception(
                u'Couldn’t record FAQ click because tool with ID {tool_id} doesn’t exist: {error}'.format(
                    tool_id=self.kwargs['tool_id'],
                    error=str(e),
                )
            )
            return HttpResponse(status=404)

        try:
            faq = Faq.objects.get(
                id=self.kwargs['faq_id'],
                publishable=True,
                tool=tool,
            )
        except Faq.DoesNotExist as e:
            logger.exception(
                u'Couldn’t record FAQ click because FAQ with id {faq_id} and tool_id {tool_id} doesn’t exist: {error}'.format(
                    faq_id=self.kwargs['faq_id'],
                    tool_id=tool.id,
                    error=str(e),
                )
            )
            return HttpResponse(status=404)

        faq.click_count += 1

        try:
            faq.save(update_fields=['click_count'])
        except Exception as e:
            logger.exception(
                u'Error when attempting to record click for tool FAQ: {error}'.format(
                    error=str(e)
                )
            )
            return HttpResponse(status=500)

        return HttpResponse(status=204)
