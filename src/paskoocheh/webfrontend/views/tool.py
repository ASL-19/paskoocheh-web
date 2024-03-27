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
from django.shortcuts import redirect
from django.views import View
from webfrontend.caches.responses.decorators import pk_cache_response
from webfrontend.mixins import ToolMixin
from webfrontend.utils.uri import get_tool_preferred_version_path


class ToolView(View, ToolMixin):
    u"""Tool view."""

    @pk_cache_response()
    def get(self, request, **kwargs):
        u"""
        Generate a base tool URL response.

        Because there is no concept of looking at a tool without also looking
        at a version, this view either displays an error message if the tool
        can’t be found, or redirects to a version of the tool.

        Args:
            **tool_id (string): tools.models.Tool.id

        Returns:
            HttpResponse
        """
        data_or_error_response = self.get_tool_data_or_error_response()

        if isinstance(data_or_error_response, HttpResponse):
            return data_or_error_response
        else:
            data = data_or_error_response

        redirect_path = get_tool_preferred_version_path(data.tool, self.request)

        return redirect(
            redirect_path,
            permanent=False,
        )
