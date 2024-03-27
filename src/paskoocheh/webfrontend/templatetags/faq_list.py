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

u"""Registers faq_list Django template tag."""

from django import template
from webfrontend.utils.general import enforce_required_args
from django.conf import settings

register = template.Library()

app = settings.PLATFORM


@register.inclusion_tag('webfrontend/tags/faq_list.html')
def faq_list(
    faqs=None,
    tool=None,
    version=None
):
    u"""
    Build the context for the faq_list inclusion tag.

    Args:
        Required:
            faqs (iterable of Faq)
            tool (Tool)
        Optional:
            version (Version): If present, FAQ permalink will be version-
                specific.

    Returns:
        dictionary: Template context
    """
    enforce_required_args(locals(), 'faqs', 'tool')

    return {
        'faqs': faqs,
        'tool': tool,
        'version': version,
        'app': app,
    }
