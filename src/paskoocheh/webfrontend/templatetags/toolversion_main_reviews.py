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

u"""Registers toolversion_main_reviews Django template tag."""

from django import template
from django.db.models.functions import Length
from stats.models import VersionReview
from webfrontend.utils.general import enforce_required_args
from webfrontend.utils.review import get_rating_options
from webfrontend.utils.uri import pask_reverse

register = template.Library()


@register.inclusion_tag(
    'webfrontend/tags/toolversion_main_reviews.html',
    takes_context=True
)
def toolversion_main_reviews(
    context,
    version=None,
    version_name_localized=None,
    rating=None,
    rating_val=None,
    rating_count=None,
    no_version_rating_available=None
):
    u"""
    Build the context for the toolversion_main_reviews inclusion tag.

    Required args:
        version (Version)
        version_name_localized (unicode)

    Returns:
        dict: Template context
    """
    enforce_required_args(locals(), 'version', 'version_name_localized')

    latest_reviews = (
        VersionReview.objects
        .annotate(
            text_len=Length('text')
        )
        .filter(
            language=context.request.LANGUAGE_CODE,
            platform_name=version.supported_os.slug_name,
            text_len__gte=3,
            tool_name=version.tool.name,
        )
        .order_by('-timestamp')
        .all()
        [:6]
    )

    has_more_reviews = False

    if latest_reviews:
        has_more_reviews = (len(latest_reviews) == 6)
        latest_reviews = latest_reviews[:5]

    for review in latest_reviews:
        review.url_path = pask_reverse(
            'webfrontend:toolversionreview',
            context.request,
            p_tool_id=version.tool.id,
            p_platform_slug=version.supported_os.slug_name,
            p_review_id=review.id
        )

    return {
        'has_more_reviews': has_more_reviews,
        'latest_reviews': latest_reviews,
        'rating_options': get_rating_options(),
        'version': version,
        'version_name_localized': version_name_localized,
        'rating': rating,
        'rating_val': rating_val,
        'rating_count': rating_count,
        'no_version_rating_available': no_version_rating_available
    }
