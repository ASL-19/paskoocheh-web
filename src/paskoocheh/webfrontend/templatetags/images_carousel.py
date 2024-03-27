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

u"""Registers images_carousel Django template tag."""

import re
from django import template
from webfrontend.utils.general import enforce_required_args

register = template.Library()


@register.inclusion_tag('webfrontend/tags/images_carousel.html')
def images_carousel(
    images=None,
    should_fit_viewport=False,
    version=None,
):
    u"""
    Build the context for the images_carousel inclusion tag.

    Most of this code has to do with pre-calculating aspect ratios. This is
    necessary (or at least the easiest way) to avoid Flickity (carousel
    library) race conditions and browser-specific layout bugs. It also reduces
    the amount of potential layout juddering and coresponding CPU-heavy reflow.

    Note that there are landscape and portrait layout modes. Portrait layout is
    triggered if there is at least one portrait image. This is in place to
    avoid carousels from filling the entire viewport when they contain potrait
    screenshots, e.g. phone screenshots.

    The should_fit_viewport functionality is currently implemented via some
    crude portrait/landscape-specific styles with hard-coded ratios. It’s
    likely going to be problematic to do properly since it will involve wading
    into inconsistent mobile browser viewport/vh implementations (e.g. iPhone
    Safari’s bottom toolbar).

    Args:
        images (List of Image)
        should_fit_viewport (bool): Should the viewport attempt to limit its
            size to fit inside the browser viewport?
        version (Version)

    Returns:
        dictionary: Template context
    """
    enforce_required_args(locals(), 'images')

    existant_images = []
    has_portrait_images = False
    largest_height_to_width_percentage = 0

    for image in images:
        if image.width > 0 and image.height > 0:
            height_to_width_percentage = (
                (float(image.height) / float(image.width)) * 100
            )

            if height_to_width_percentage > largest_height_to_width_percentage:
                largest_height_to_width_percentage = height_to_width_percentage

            if height_to_width_percentage > 100:
                has_portrait_images = True

            image.inline_style = (
                "display: block; content: ' '; padding-bottom: {height_to_width_percentage}%;".format(
                    height_to_width_percentage=height_to_width_percentage
                )
            )

            image.link_is_external = bool(
                hasattr(image, 'link') and
                image.link and
                re.match(r'https?:\/\/', image.link)
            )

            existant_images.append(image)

    if has_portrait_images:
        container_padding_bottom_percentage_narrow = (
            largest_height_to_width_percentage * 0.6
        )
        container_padding_bottom_percentage_wide = (
            largest_height_to_width_percentage * 0.4
        )
    else:
        container_padding_bottom_percentage_narrow = (
            largest_height_to_width_percentage
        )
        container_padding_bottom_percentage_wide = (
            largest_height_to_width_percentage * 0.6
        )

    return {
        'container_padding_bottom_percentage_narrow': (
            container_padding_bottom_percentage_narrow
        ),
        'container_padding_bottom_percentage_wide': (
            container_padding_bottom_percentage_wide
        ),
        'has_portrait_images': has_portrait_images,
        'images': existant_images,
        'should_fit_viewport': should_fit_viewport,
        'version': version,
    }
