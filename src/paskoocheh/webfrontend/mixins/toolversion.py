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
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.utils.translation import pgettext
from tools.models import Tool, Version
from webfrontend.utils.general import SUPPORTED_PLATFORM_SLUG_NAMES
from webfrontend.utils.uri import pask_reverse
from django.conf import settings

app = settings.PLATFORM


@attr.s(frozen=True, slots=True)
class ToolVersionData(object):
    u"""
    Immutable object containing data useful for a Version-specific view.

    Attributes:
        tool (Tool)
        tool_info (Info)
        tool_name_localized (unicode): e.g. 'TunnelBear'
        tool_version (Version)
        tool_versions (QuerySet of Version)
        version_name_localized (Tool): e.g. 'TunnelBear for Android'
    """
    tool = attr.ib()
    tool_info = attr.ib()
    tool_name_localized = attr.ib()
    tool_version = attr.ib()
    tool_versions = attr.ib()
    version_name_localized = attr.ib()


class ToolVersionMixin(object):
    def get_tool_version_data_or_error_response(self, linux32_allowed=False, windows32_allowed=False, **kwargs):  # noqa: C901
        u"""
        Attempt to parse the request and get the various data necessary to
        display a tool version page.

        Returns:
            If required arguments exist and queries are successful:
                ToolVersionData
            Else:
                webfrontend.PageNotFoundView (HttpResponse)
        """
        from webfrontend.views import PageNotFoundView

        if self.kwargs['platform_slug'] == 'osx':
            return redirect(
                pask_reverse(
                    'webfrontend:toolversion',
                    self.request,
                    p_tool_id=self.kwargs['tool_id'],
                    p_platform_slug='macos'
                ),
                permanent=True
            )

        if (
            # Respond as though “linux32”/"windows32" doesn’t exist unless
            # linux32_allowed/windows32_allowed argument passed.
            # This prevents users from manually accessing
            # 32bit OS views, submitting 32-bit OS reviews, etc., while still
            # allowing linux32/windows32 downloads in ToolVersionDownloadView.
            (
                self.kwargs['platform_slug'] == 'linux32' and
                not linux32_allowed
            ) or
            (
                self.kwargs['platform_slug'] == 'windows32' and
                not windows32_allowed
            ) or
            self.kwargs['platform_slug'] not in SUPPORTED_PLATFORM_SLUG_NAMES
        ):
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'URL contains unknown platform code “{platform_code}”.',
                    )
                    .format(
                        platform_code=self.kwargs['platform_slug']
                    )
                )
            )

        # Look up Tool and Version ContentTypes as once, rather than
        # allowing separate lookups. Content types lookups are cached so we
        # don’t need to store them.
        ContentType.objects.get_for_models(Tool, Version)

        if kwargs.get('include_tool_versions', False):
            tool_versions_queryset = (
                Version.objects
                .select_related('supported_os', 'tool')
                .filter(
                    publishable=True,
                    tool__publishable=True,
                    tool_id=self.kwargs['tool_id'],
                )
            )

            tool_versions = tool_versions_queryset.all()

            if len(tool_versions) == 0:
                return PageNotFoundView.as_view()(
                    self.request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            u'No tool matching this URL exists. The tool may no longer be listed.',
                        )
                    )
                )

            tool_version = None
            for version in tool_versions:
                if version.supported_os.slug_name == self.kwargs['platform_slug']:
                    tool_version = version
                    break

            if not tool_version:
                return PageNotFoundView.as_view()(
                    self.request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            u'The requested version of this tool doesn’t exist. The version may be discontinued or removed.',
                        )
                    )
                )
        else:
            try:
                tool_version = (
                    Version.objects
                    .select_related('tool', 'supported_os')
                    .get(
                        publishable=True,
                        supported_os__slug_name=self.kwargs['platform_slug'],
                        tool__publishable=True,
                        tool_id=self.kwargs['tool_id'],
                    )
                )
            except Version.DoesNotExist:
                return PageNotFoundView.as_view()(
                    self.request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            u'No tool matching this URL exists. The tool may no longer be listed.',
                        )
                    )
                )

            tool_versions = None

        tool = tool_version.tool

        # Get language-specific tool info, which is stored in a separate table
        tool_info = tool.infos.filter(
            language=self.request.LANGUAGE_CODE,
            publishable=True,
        ).first()

        tool_name_localized = tool_info.name if tool_info else tool.name
        platform_name = tool_version.supported_os.display_name_ar if app == 'zanga' else tool_version.supported_os.display_name_fa

        version_name_localized = (
            pgettext(
                u'Tool version',
                # Translators: Used to format tool version title
                u'{tool_name} for {platform_name}'
            )
            .format(
                tool_name=tool_name_localized,
                platform_name=platform_name,
            )
        )

        return ToolVersionData(
            tool=tool,
            tool_name_localized=tool_name_localized,
            tool_info=tool_info,
            tool_version=tool_version,
            version_name_localized=version_name_localized,
            tool_versions=tool_versions,
        )
