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

u"""Registers main_footer Django template tag."""

from django import template
from django.conf import settings
from preferences.models import GeneralPreference
register = template.Library()

app = settings.PLATFORM


@register.inclusion_tag(
    'webfrontend/tags/main_footer.html',
    takes_context=True
)
def main_footer(context):
    u"""
    Build the context for the main_footer inclusion tag.

    Args:
        context (RequestContext) (injected by decorator)

    Returns:
        dictionary: Template context
    """
    current_page_slug = None
    if 'slug' in context['request'].resolver_match.kwargs:
        current_page_slug = context['request'].resolver_match.kwargs['slug']

    current_view_name = context['request'].resolver_match.url_name

    support_email = None
    twitter = None
    facebook = None
    instagram = None
    telegram = None

    if GeneralPreference.objects.first():
        obj = GeneralPreference.objects.first()
        support_email = getattr(obj, 'support_email', None)
        twitter = getattr(obj, 'twitter', None)
        facebook = getattr(obj, 'facebook', None)
        instagram = getattr(obj, 'instagram', None)
        telegram = getattr(obj, 'telegram', None)

    EMAIL_LIST_URL = settings.EMAIL_LIST_URL
    EMAIL_LIST_HIDDEN = settings.EMAIL_LIST_HIDDEN

    return {
        'current_page_slug': current_page_slug,
        'current_view_name': current_view_name,
        'support_email': support_email,
        'twitter': twitter,
        'facebook': facebook,
        'instagram': instagram,
        'telegram': telegram,
        'EMAIL_LIST_URL': EMAIL_LIST_URL,
        'EMAIL_LIST_HIDDEN': EMAIL_LIST_HIDDEN,
        'app': app,
    }
