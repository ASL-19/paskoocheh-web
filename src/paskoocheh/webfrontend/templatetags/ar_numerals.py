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

u"""Registers ar_numerals Django template filter."""

from django import template
from webfrontend.utils.general import replace_wa_numerals_with_ar_numerals

register = template.Library()


@register.filter()
def ar_numerals(input):
    u"""
    Return input string with all Western Arabic numerals replaced by
    Arabic numerals.

    See https://en.wikipedia.org/wiki/Eastern_Arabic_numerals

    Args:
        input (str)
    Returns:
        str
    """
    return replace_wa_numerals_with_ar_numerals(input)
