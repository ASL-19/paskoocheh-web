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

import attr
from django.utils.translation import pgettext
from tools.models import Tool


@attr.s(frozen=True, slots=True)
class ToolData(object):
    u"""
    Immutable object containing data useful for a Tool-specific view.

    Attributes:
        tool (Tool)
        tool_info (Info)
        tool_name_localized (unicode)
    """
    tool = attr.ib()
    tool_info = attr.ib()
    tool_name_localized = attr.ib()


class ToolMixin(object):
    u"""Mixin for any view that gets a tool."""
    def get_tool_data_or_error_response(self):
        u"""
        Attempt to parse the request and get the various data necessary to
        display a tool page.

        Returns:
            If required arguments exist and queries are successful:
                ToolData
            Else:
                webfrontend.PageNotFoundView (HttpResponse)
        """

        try:
            tool = Tool.objects.get(
                id=self.kwargs['tool_id'],
                publishable=True,
            )
        except Tool.DoesNotExist:
            return self.get_no_matching_tool_error_response()

        publishable_versions = (
            tool.versions.filter(
                publishable=True,
            )
        )

        if publishable_versions.count() == 0:
            return self.get_no_matching_tool_error_response()

        tool_info = tool.infos.filter(
            language=self.request.LANGUAGE_CODE,
            publishable=True,
        ).first()

        if tool_info is not None:
            tool_name_localized = tool_info.name
        else:
            tool_name_localized = tool.name

        return ToolData(
            tool=tool,
            tool_info=tool_info,
            tool_name_localized=tool_name_localized,
        )

    def get_no_matching_tool_error_response(self):
        from webfrontend.views import PageNotFoundView

        return PageNotFoundView.as_view()(
            self.request,
            error_message=(
                pgettext(
                    u'Error message',
                    u'No tool matching this URL exists. The tool may no longer be listed.',
                )
            )
        )
