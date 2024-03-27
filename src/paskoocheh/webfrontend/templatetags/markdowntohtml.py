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

u"""Registers markdowntohtml Django template filter."""

from django import template
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

register = template.Library()


@register.filter(is_safe=True)
def markdowntohtml(markdown_text):
    u"""
    Render a Markdown string as an HTML SafeText.

    Args:
        markdown_text (str): Unprocessed Markdown text

    Returns:
        SafeText
    """
    markdown_html = markdownify(markdown_text)
    safe_markdown_html = mark_safe(markdown_html)
    return safe_markdown_html
