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

u"""Registers webfrontend’s custom Django template tags."""

from django import template
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.translation import pgettext
from tools.models import Image, Tool
from webfrontend.utils.uri import (
    get_tool_preferred_version_path,
    pask_reverse,
)
from django.conf import settings

app = settings.PLATFORM

register = template.Library()


@register.inclusion_tag(
    'webfrontend/tags/blog_associated_tool_list_item.html',
    takes_context=True,
)
def blog_associated_tool_list_item(
    context,
    tool=None,
    version=None,
):
    u"""
    Build the context for the blog_associated_tool_list_item inclusion tag.

    Args:
        Optional:
            tool (Tool)
            version (Version)

    Returns:
        dictionary: Template context
    """
    if not tool and not version:
        raise TypeError('Must provide tool or version.')
    if tool and version:
        raise TypeError('Must not provide both tool and version.')

    _tool = version.tool if version else tool

    tool_info = _tool.infos.filter(
        language=context.request.LANGUAGE_CODE,
        publishable=True,
    ).first()

    tool_name_localized = tool_info.name if tool_info else tool.name

    logo = (
        Image.objects
        .filter(
            Q(publish=True) &
            (
                Q(language__isnull=True) |
                Q(language=context.request.LANGUAGE_CODE)
            ) &
            (
                Q(content_type=ContentType.objects.get_for_model(Tool)) &
                Q(object_id=_tool.id) &
                Q(image_type='logo')
            )
        )
        .order_by('order')
        .first()
    )

    displayed_name = None
    link = None

    if version:
        platform_name = version.supported_os.display_name_ar if app == 'zanga' else version.supported_os.display_name_fa
        displayed_name = (
            pgettext(
                u'Blog post associated tool',
                # Translators: The name used for a Version in the associated
                # Versions/Tools list at the bottom of blog posts. Note that
                # both Tools and Versons can be associated with Posts. If a
                # Tool is associated, it’s listed as just {tool_name}, which
                # doesn’t require a translation.
                u'{tool_name} for {platform_name}'
            )
            .format(
                tool_name=tool_name_localized,
                platform_name=platform_name,
            )
        )
        link = pask_reverse(
            'webfrontend:toolversion',
            context.request,
            p_tool_id=version.tool.id,
            p_platform_slug=version.supported_os.slug_name,
        )
    else:
        displayed_name = tool_name_localized
        link = get_tool_preferred_version_path(tool, context.request)

    logo_path = None
    if logo:
        logo_path = logo.image.url

    default_image_path = settings.WEBFRONTEND_DEFAULT_IMAGE_PATH

    return {
        'link': link,
        'logo_path': logo_path,
        'name': displayed_name,
        'default_image_path': default_image_path,
    }
