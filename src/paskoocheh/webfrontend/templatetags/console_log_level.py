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

u"""Registers console_log_level Django template tag."""

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def console_log_level():
    u"""Read Django log level setting and return int used by setUpConsole JS
    function.

    Args:
       request (HTTPRequest)

    Returns:
        int between 1 and 4
    """
    if settings.LOG_LEVEL == 'DEBUG':
        console_log_level = 4
    elif settings.LOG_LEVEL == 'INFO':
        console_log_level = 4
    elif settings.LOG_LEVEL == 'WARNING':
        console_log_level = 2
    else:
        console_log_level = 1

    return console_log_level
