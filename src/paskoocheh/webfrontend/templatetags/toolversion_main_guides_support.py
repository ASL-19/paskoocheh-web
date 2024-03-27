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

u"""Registers toolversion_main_guides_support Django template tag."""

from django import template
from webfrontend.utils.general import enforce_required_args

register = template.Library()


@register.inclusion_tag(
    'webfrontend/tags/toolversion_main_guides_support.html',
    takes_context=True
)
def toolversion_main_guides_support(
    context,
    blog_posts=None,
    faqs=None,
    tutorials=None,
    version=None,
    version_has_guide=False,
    version_name_localized=None,
):
    u"""
    Build the context for the toolversion_main_guides_support inclusion tag.

    Required args:
        version (Version)
        version_name_localized (unicode)

    Optional args:
        faqs (iterable of Faq)
        tutorials (iterable of Tutorial)
        version_has_guide (bool)

    Returns:
        dict: Template context
    """
    enforce_required_args(locals(), 'version', 'version_name_localized')

    blogpostsview_version_code = '{tool_id}-{platform_slug_name}'.format(
        tool_id=version.tool.id,
        platform_slug_name=version.supported_os.slug_name,
    )

    return {
        'blogpostsview_version_code': blogpostsview_version_code,
        'blog_posts': blog_posts,
        'faqs': faqs,
        'tutorials': tutorials,
        'version': version,
        'version_has_guide': version_has_guide,
        'version_name_localized': version_name_localized,
    }
