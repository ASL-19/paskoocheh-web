# -*- coding: utf-8 -*-
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

import hashlib
import logging

from datetime import datetime
# from django.core.exceptions import DoesNotExist
from .tasks import (
    insert_download,
    insert_feedback,
    insert_rating,
)
from tools.models import Version

logger = logging.getLogger(__name__)


def save_rating(**kwargs):
    """
        Record a rating from user

        kwargs: kwargs for the function:
            'version_id': id of the Version being rated
            'channel_version': version of webapp
            'rating': rating value posted by the user
            'title': title of the review
            'text': text of the review
            'user_id': ID of the user posting the review,
            'request_ip': IP address of the review request (use
                paskoocheh.helpers.get_client_ip),
    """
    try:
        rating = kwargs['rating']
        request_ip = kwargs['request_ip']
        version_id = kwargs['version_id']
    except KeyError as error:
        raise TypeError(
            'Missing required ' + error.args[0] + ' keyword argument'
        )

    channel_version = kwargs.get('channel_version', None)
    text = kwargs.get('text', None)
    title = kwargs.get('title', None)
    user_id = kwargs.get('user_id', None)
    language = kwargs.get('language', None)

    try:
        ver = Version.objects.get(pk=version_id)
    except Version.DoesNotExist:
        raise Version.DoesNotExist(
            'Version with ID {} does not exist'.format(str(version_id))
        )

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_uuid = hashlib.sha512(request_ip).hexdigest()

    insert_rating(
        user_uuid,
        user_id,
        timestamp,
        ver.tool.id,
        ver.tool.name,
        ver.supported_os.slug_name,
        ver.version_number,
        channel_version,
        rating,
        title,
        text,
        language)

    return True


def save_feedback(**kwargs):
    """
        Record a feedback from user

        kwargs: kwargs for the function:
            'channel_version': version of webapp
            'title': title of the feedback
            'text': text of the feedback
            'user_id': ID of the user posted the feedback,
            'request_ip': IP address of the feedback request (use
                paskoocheh.helpers.get_client_ip),
    """
    try:
        request_ip = kwargs['request_ip']
        title = kwargs['title']
        text = kwargs['text']
        user_id = kwargs['user_id']
    except KeyError as error:
        raise TypeError(
            'Missing required ' + error.args[0] + ' keyword argument'
        )

    channel_version = kwargs.get('channel_version', None)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_uuid = hashlib.sha512(request_ip).hexdigest()

    insert_feedback(
        user_uuid,
        timestamp,
        title,
        text,
        user_id,
        channel_version)

    return True


def save_download(**kwargs):
    """
        Record a download from user

        kwargs: kwargs for the function:
            'version_id': id of the Version downloaded
            'channel_version': version of webapp
            'downloaded_via': source of download
            'request_ip': IP address of the feedback request (use
                paskoocheh.helpers.get_client_ip),
    """
    try:
        request_ip = kwargs['request_ip']
        version_id = kwargs['version_id']
        downloaded_via = kwargs['downloaded_via']
    except KeyError as error:
        raise TypeError(
            'Missing required ' + error.args[0] + ' keyword argument'
        )

    channel_version = kwargs.get('channel_version', None)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_uuid = hashlib.sha512(request_ip).hexdigest()

    try:
        ver = Version.objects.get(pk=version_id)
    except Version.DoesNotExist:
        raise Version.DoesNotExist(
            'Version with ID {} does not exist'.format(str(version_id))
        )

    version_size = 0
    version_codes = ver.version_codes.all()
    if version_codes:
        version_size = ver.version_codes.first().size

    insert_download(
        user_uuid,
        timestamp,
        ver.tool.name,
        ver.tool.id,
        ver.supported_os.slug_name,
        ver.version_number,
        version_size,
        downloaded_via,
        channel_version)

    return True
