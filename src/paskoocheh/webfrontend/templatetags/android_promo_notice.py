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

u"""Registers android_promo_notice template tag."""

from django import template
from webfrontend.utils.uri import pask_reverse

register = template.Library()


@register.inclusion_tag(
    'webfrontend/tags/android_promo_notice.html',
    takes_context=True,
)
def android_promo_notice(context):
    u"""
    Build the context for the android_promo_notice inclusion tag.

    Returns:
        dictionary: Template context
    """

    paskoocheh_android_download_url = pask_reverse(
        'webfrontend:toolversiondownload',
        context.request,
        p_tool_id=42,
        p_platform_slug='android',
    )

    return {
        'paskoocheh_android_download_url': paskoocheh_android_download_url,
    }
