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

u"""Registers pk_request_is_noop_value Django template tag."""

from django import template
from webfrontend.utils.general import is_request_user_agent_noop

register = template.Library()


@register.simple_tag(takes_context=True)
def pk_request_is_noop_value(context):
    u"""
    Returns value of is_request_user_agent_noop()
    """
    return is_request_user_agent_noop(context.request)
