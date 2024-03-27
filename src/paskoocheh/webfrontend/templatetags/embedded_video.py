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

u"""Registers embedded_video Django template tag."""

import attr
from django import template
from webfrontend.utils.general import enforce_required_args
from django.conf import settings
from tools.models import Version, Tutorial

register = template.Library()


@register.inclusion_tag('webfrontend/tags/embedded_video.html')
def embedded_video(
    content_object=None,
    is_lazy_loading=False,
    in_carousel=False,
    js_container_elem_prefix=None
):
    u"""
    Build the context for the embedded_video inclusion tag.

    Required args:
        content_object (object): an instance of type Version or Tutorial

    Optional args:
        is_lazy_loading (bool): True if video is inside an expandable list and
            should be lazy-loaded when its containing list item is opened
        in_carousel (bool): True if video is inside an images-carousel
        js_container_elem_prefix (str): a prefix for the containing element of
            the embedded video <iframe> (needed for youtube and vimeo videos)
    Returns:
        dictionary: Template context
    """
    enforce_required_args(locals(), 'content_object')

    parsed_video_info = None
    video_path = None
    is_version_or_tutorial_object = isinstance(content_object, Version) or isinstance(content_object, Tutorial)

    if is_version_or_tutorial_object and content_object.video_link:
        parsed_video_info = parse_video_url(content_object.video_link)
    elif content_object.video:
        video_path = f'{settings.MEDIA_URL}{content_object.video}'

    return {
        'is_lazy_loading': str(is_lazy_loading).lower(),
        'parsed_video_info': parsed_video_info,
        'content_object': content_object,
        'video_path': video_path,
        'in_carousel': in_carousel,
        'js_container_elem_prefix': js_container_elem_prefix,
    }


@attr.s(frozen=True, slots=True)
class VideoMetadata(object):
    u"""
    Immutable object containing metadata about a video URL.

    Attributes:
        video_type ('youtube', 'vimeo', 'file', or None if no match)
        external_video_id (str or None): Video ID for external service, or
            None if no match
    """
    external_id = attr.ib()
    type = attr.ib()


def parse_video_url(video_url):
    u"""
    Parses a video URL, returns the video type and external service (YouTube, Vimeo) video ID

    Args:
        video_url (str): Video

    Returns:
        webfrontend.utils.general.VideoMetadata
    """
    import re

    youtube_video_id_matches = re.match(
        r'https:\/\/www\.youtube\.com\/watch\?.*v=([^&]*)',
        video_url
    )

    if (youtube_video_id_matches):
        return VideoMetadata(
            external_id=youtube_video_id_matches.group(1),
            type='youtube',
        )

    vimeo_video_id_matches = re.match(
        r'https:\/\/vimeo\.com\/(\d+).*',
        video_url
    )

    if (vimeo_video_id_matches):
        return VideoMetadata(
            external_id=vimeo_video_id_matches.group(1),
            type='vimeo',
        )

    return VideoMetadata(
        external_id=None,
        type=None,
    )
