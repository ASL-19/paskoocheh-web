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
from tools.models import Faq
from webfrontend.caches.responses.decorators import pk_cache_response
from webfrontend.mixins import ToolMixin
from webfrontend.templatetags.pk_meta_tags import PkViewMetadata
from webfrontend.utils.general import (
    wrap_with_link,
)
from webfrontend.utils.query import (
    add_select_related_to_faqs_queryset,
)
from webfrontend.utils.uri import (
    get_tool_preferred_version_path,
)


class ToolFaqsView(View, ToolMixin):
    u"""View for tool version FAQs page."""

    @pk_cache_response()
    def get(self, request, **kwargs):
        u"""
        Generate a tool FAQs page response.

        Get the tool data and tool FAQs matching the named
        group arguments, render the tool FAQs page.

        Args:
            **tool_id (string): tools.models.Tool.id

        Returns:
            HttpResponse
        """
        data_or_error_response = self.get_tool_data_or_error_response()

        if isinstance(data_or_error_response, HttpResponse):
            return data_or_error_response
        else:
            tool_data = data_or_error_response

        faqs = add_select_related_to_faqs_queryset(
            Faq.objects
            .filter(
                language=self.request.LANGUAGE_CODE,
                publishable=True,
                tool=tool_data.tool,
            )
            .order_by('order')
        )

        preferred_tool_version_path = get_tool_preferred_version_path(
            tool_data.tool,
            self.request
        )

        page_heading_inner_html = (
            pgettext(
                u'FAQ',
                # Translators: Title of tool or tool version FAQs listing (e.g.
                # /tools/42/faqs/ or /tools/42/android/faqs/)
                u'FAQs for {tool_name}',
            )
            .format(
                tool_name=wrap_with_link(
                    tool_data.tool_name_localized,
                    preferred_tool_version_path,
                )
            )
        )

        page_title = (
            pgettext(
                u'FAQ',
                u'FAQs for {tool_name}',
            )
            .format(
                tool_name=tool_data.tool_name_localized
            )
        )

        view_metadata = PkViewMetadata(
            title=page_title,
        )

        return render(
            self.request,
            'webfrontend/toolfaqs.html',
            context={
                'faqs': faqs,
                'page_heading_inner_html': page_heading_inner_html,
                'page_title': page_title,
                'tool': tool_data.tool,
                'view_metadata': view_metadata,
            }
        )
