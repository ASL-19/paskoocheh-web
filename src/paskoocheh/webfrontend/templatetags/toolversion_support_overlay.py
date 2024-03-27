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

u"""Registers toolversion_support_overlay Django template tag."""

from django import template
from django.utils.translation import pgettext
from webfrontend.utils.general import enforce_required_args
from django.conf import settings

register = template.Library()

app = settings.PLATFORM


@register.inclusion_tag('webfrontend/tags/toolversion_support_overlay.html')
def toolversion_support_overlay(
    tool=None,
    tool_logo=None,
    version=None,
    version_name_localized=None,
):
    u"""
    Build the context for the toolversion_review_overlay incusion tag.

    Required args:
        tool (Tool)
        tool_logo (Image)
        version (Version)
        version_name_localized (unicode)

    Returns:
        dict: Template context
    """
    enforce_required_args(locals(), 'tool', 'version', 'version_name_localized')

    overlay_slug = 'pk-toolversion-support-overlay'
    overlay_title = (
        pgettext(
            u'Support overlay',
            # Translators: Overlay title
            u'Get support for {tool_name_and_platform}',
        )
        .format(
            tool_name_and_platform=version_name_localized,
        )
    )

    overlay_subtitle = (
        pgettext(
            u'Support overlay',
            # Translators: Overlay subtitle
            u'We promise to respond as soon as possible',
        )
    )

    return {
        'overlay_slug': overlay_slug,
        'overlay_title': overlay_title,
        'overlay_subtitle': overlay_subtitle,
        'tool': version.tool,
        'tool_version': version,
        'app': app,
        'tool_logo': tool_logo,
    }
