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

u"""webfrontend review utilities."""

import attr
from django.utils.translation import npgettext


@attr.s(frozen=True, slots=True)
class ReviewFormRatingOption(object):
    u"""
    Immutable object describing a review form rating <option>.

    Attributes:
        text (str): Localized textual description of rating (e.g. '3 stars')
        value (float)
    """
    text = attr.ib()
    value = attr.ib()


def get_rating_options():
    u'''
    Generates a list of ReviewFormRatingOption, including translated text
    values.

    Returns:
        list of ReviewFormRatingOption
    '''
    rating_options = []
    for i in range(11):
        rating = float(i) / 2

        rating_options.append(
            ReviewFormRatingOption(
                text=(
                    npgettext(
                        u'Review',
                        # Translators: Selections in the review form rating
                        # drop-down
                        u'{rating} star',
                        u'{rating} stars',
                        rating
                    )
                    .format(
                        rating=rating
                    )
                ),
                value=rating,
            )
        )

    return rating_options
