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

u"""Registers settings_value Django template tag."""

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def settings_value(setting_key):
    u"""
    Returns the value of the provided settings key.

    Arguments:
        setting_key (str): e.g. 'GRECAPTCHA_INVISIBLE_SITE_KEY'

    Returns:
        Path and query string (str)
    """
    return getattr(settings, setting_key, '')
