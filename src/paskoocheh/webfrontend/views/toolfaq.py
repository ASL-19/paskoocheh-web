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
from webfrontend.utils.uri import (
    get_tool_preferred_version_path,
)


class ToolFaqView(View, ToolMixin):
    u"""View for tool FAQ page."""

    @pk_cache_response()
    def get(self, request, **kwargs):
        u"""
        Generate a tool FAQ page response.

        Get the tool data and tool FAQ matching the named group arguments,
        render the tool FAQ page.

        Args:
            **tool_id (string): tools.models.Tool.id
            **faq_id (string): tools.models.Faq.id

        Returns:
            HttpResponse
        """
        from webfrontend.views import PageNotFoundView

        data_or_error_response = self.get_tool_data_or_error_response()

        if isinstance(data_or_error_response, HttpResponse):
            return data_or_error_response
        else:
            tool_data = data_or_error_response

        try:
            faq = Faq.objects.get(
                id=self.kwargs['faq_id'],
                publishable=True,
                tool=tool_data.tool
            )
        except Faq.DoesNotExist:
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'No FAQ matching this URL exists.',
                    )
                ),
            )

        footer_p_inner_html = (
            pgettext(
                u'FAQ',
                # Translators: Appears beneath FAQ question/title
                u'FAQ for {tool_name}'
            )
            .format(
                tool_name=wrap_with_link(
                    tool_data.tool_name_localized,
                    get_tool_preferred_version_path(
                        tool_data.tool,
                        self.request
                    )
                )
            )
        )

        view_metadata = PkViewMetadata(
            description=(faq.body if faq.body else False),
            description_is_markdown=bool(faq.body),
            title=faq.headline,
        )

        return render(
            self.request,
            'webfrontend/toolfaq.html',
            context={
                'faq': faq,
                'footer_p_inner_html': footer_p_inner_html,
                'tool': tool_data.tool,
                'tool_name_localized': tool_data.tool_name_localized,
                'view_metadata': view_metadata,
            }
        )
