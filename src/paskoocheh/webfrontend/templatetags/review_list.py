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

u"""Registers review_list Django template tag."""

from django import template
from django.utils.translation import pgettext
from webfrontend.utils.general import enforce_required_args

register = template.Library()


@register.inclusion_tag('webfrontend/tags/review_list.html')
def review_list(
    review_invisible_heading_tag=None,
    reviews=None,
    version_name_localized=None
):
    u"""
    Build the context for the review_list inclusion tag.

    Required args:
        reviews (iterable of VersionReview)
        version_name_localized (str): Localized name of tool version, e.g.
            'Privacy Badger for Firefox'
    Optional args:
        review_invisible_heading_tag (str): Optional tag name of invisible
            review heading, if wanted. e.g. 'h3'.

    Returns:
        dictionary: Template context
    """
    enforce_required_args(locals(), 'reviews', 'version_name_localized')

    review_invisible_heading_text = (
        pgettext(
            u'Review',
            # Translators: Single review title
            u'Review for {tool_name_and_version}',
        )
        .format(
            tool_name_and_version=version_name_localized
        )
    )

    return {
        'review_invisible_heading_tag': review_invisible_heading_tag,
        'review_invisible_heading_text': review_invisible_heading_text,
        'reviews': reviews,
        'version_name_localized': version_name_localized,
    }
