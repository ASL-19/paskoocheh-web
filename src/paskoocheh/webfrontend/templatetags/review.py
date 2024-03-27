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

u"""Registers review Django template tag."""

from django import template
from django.utils.translation import npgettext
from webfrontend.utils.general import (
    enforce_required_args,
    gregorian_datetime_to_jalali_date_string,
    replace_wa_numerals_with_pa_numerals
)
from django.conf import settings

app = settings.PLATFORM

register = template.Library()


@register.inclusion_tag('webfrontend/tags/review.html')
def review(
    h1_inner_html=None,
    invisible_heading_tag=None,
    invisible_heading_text=None,
    review=None,
    url_path=None,
):
    u"""
    Build the context for the review inclusion tag.

    Required args:
        review (VersionReview)

    Optional args:
        h1_inner_html (unicode): If provided, review will include an <h1>
            containing the provided HTML, which should describe the review
            (HTML is allowed so <h1> can include a link to the version page)
        invisible_heading_tag (unicode): Semantically-appropriate tag for a
            hidden heading element. Requires invisible_heading_text to be set
            and h1_inner_html to be missing.
        invisible_heading_text (unicode): Title of the review, to be contained
            inside invisible_heading_tag. Requires invisible_heading_tag to be
            set and h1_inner_html to be missing.
        url_path (unicode): If provided, review footer will link to this path.

    Returns:
        dictionary: Template context
    """
    enforce_required_args(locals(), 'review')

    review_timestamp_iso8601 = (
        review.timestamp
        .replace(microsecond=0)
        .isoformat()
    )
    review_timestamp_jalali = gregorian_datetime_to_jalali_date_string(
        review.timestamp
    )

    rating_inner_html = (
        npgettext(
            u'Review',
            # Translators: Used to generate the rating text (next to the star
            # icon) for reviews. Be sure to retain “<span class="invisible"> ”
            # and “</span>”, including the space after the first “>” and before
            # “star(s)”. The <span> code is there for accessibility/SEO – it’s
            # not visible, but it’s necessary to provide context for the number
            # to search engines and non-sighted users who can’t see the star
            # icon.
            u'{rating}<span class="invisible"> star</span>',
            u'{rating}<span class="invisible"> stars</span>',
            review.rating
        )
        .format(
            rating=review.rating if app == 'zanga' else replace_wa_numerals_with_pa_numerals(review.rating)
        )
    )

    return {
        'h1_inner_html': h1_inner_html,
        'invisible_heading_text': invisible_heading_text,
        'invisible_heading_tag': invisible_heading_tag,
        'rating_inner_html': rating_inner_html,
        'review': review,
        'review_url_path': url_path,
        'review_timestamp_iso8601': review_timestamp_iso8601,
        'review_timestamp_jalali': review_timestamp_jalali,
        'app': app,
    }
