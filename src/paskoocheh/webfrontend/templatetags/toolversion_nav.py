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

u"""Registers toolversion_nav Django template tag."""

import icu
from django import template
from webfrontend.utils.general import enforce_required_args
from django.conf import settings

register = template.Library()

app = settings.PLATFORM


@register.inclusion_tag('webfrontend/tags/toolversion_nav.html')
def toolversion_nav(
    active_version=None,
    available_versions=None,
    tool_name_localized=None,
    extensions_only=None,
):
    u"""
    Build the context for the toolversion_nav inclusion tag.

    Required args:
        active_version (Version)
        all_versions (list of Version)
        tool_name_localized (str): Localized name of tool (e.g. 'Privacy
            Badger')

    Returns:
        dictionary: Template context
    """
    enforce_required_args(
        locals(),
        'active_version',
        'available_versions',
        'tool_name_localized',
    )

    if app == 'zanga':
        icu_transliterator = icu.Transliterator.createInstance('Arabic-Latin/BGN')
    else:
        icu_transliterator = icu.Transliterator.createInstance('Persian-Latin/BGN')

    extension_platforms = ['chrome', 'firefox']
    if extensions_only:
        available_versions = [v for v in available_versions if v.supported_os.slug_name in extension_platforms]
    else:
        available_versions = [v for v in available_versions if v.supported_os.slug_name not in extension_platforms]

    sorted_available_versions = (
        sorted(
            available_versions,
            key=lambda version: icu_transliterator.transliterate(version.supported_os.display_name_ar or version.supported_os.display_name if app == 'zanga' else version.supported_os.display_name_fa)
        )
    )

    return {
        'active_version_id': active_version.id,
        'sorted_available_versions': sorted_available_versions,
        'tool_name_localized': tool_name_localized,
        'app': app,
    }
