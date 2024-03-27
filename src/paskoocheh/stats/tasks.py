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


import pytz
import logging
from django.conf import settings
from stats.signals import post_batch_update
from pyskoocheh import errors

app = settings.PLATFORM
logger = logging.getLogger(__name__)


def backoff(attempts):
    """
        Return a backoff delay, in seconds, given a number of attempts.

        The delay increases very rapidly with the number of attemps.
    """
    return 2 ** attempts


def get_tool(tool_id, tool_name):
    """
        Retrieves the tool id using tool name

        Args:
        tool_id: ID of the tool
        tool_name: Name of the tool

        Returns:
        The Tool record
    """

    from tools.models import Tool

    tool = None
    try:
        if tool_id is not None:
            tool = Tool.objects.get(pk=tool_id)
        else:
            tool = Tool.objects.get(name__iexact=tool_name)
    except Exception as exc:
        logger.error('Error retrieving the tool with name = {} error = {}'.format(tool_name, str(exc)))
        tool = None

    return tool


def update_download(self):
    """
        Update the download table from api_engine
        database.
    """

    from .models import StatsLastRecords, VersionDownload
    from .api_engine import query_download
    from tools.configfile import update_download_rating_json

    last_recs, created = StatsLastRecords.objects.get_or_create()

    try:
        highest_id, ndownload = query_download(last_recs.download_last)
    except Exception as exc:
        raise self.retry(countdown=backoff(self.request.retries), exc=exc)

    if highest_id is None or ndownload is None:
        return

    last_recs.download_last = highest_id
    last_recs.save()

    for dl in ndownload:

        tool = get_tool(dl.tool_id, dl.tool)
        if tool is None:
            logger.error('Tool does not exist Record {}'.format(str(dl)))
            continue

        obj, created = VersionDownload.objects.get_or_create(
            tool=tool,
            platform_name=dl.platform)
        if created:
            obj.download_count = dl.count
        else:
            obj.download_count += dl.count

        obj.tool_name = tool.name
        obj.save()

    if settings.BUILD_ENV != 'local':
        update_download_rating_json()

    post_batch_update.send(sender=VersionDownload)


def update_rating(self):
    """
        Update the rating table from api_engine
        database.
    """

    from .models import StatsLastRecords, VersionRating
    from .api_engine import query_rating
    from tools.configfile import update_download_rating_json

    last_recs, created = StatsLastRecords.objects.get_or_create()

    try:
        highest_id, nrating = query_rating(last_recs.rating_last)
    except Exception as exc:
        raise self.retry(countdown=backoff(self.request.retries), exc=exc)

    if highest_id is None or nrating is None:
        return

    last_recs.rating_last = highest_id
    last_recs.save()

    for rt in nrating:

        tool = get_tool(rt.tool_id, rt.tool)
        if tool is None:
            logger.error('Tool does not exist Record {}'.format(str(rt)))
            continue

        obj, created = VersionRating.objects.get_or_create(
            tool=tool,
            platform_name=rt.platform)

        obj.rating_count = rt.count
        obj.tool_name = tool.name
        obj.star_rating = rt.star
        obj.save()

    if settings.BUILD_ENV != 'local':
        update_download_rating_json()

    post_batch_update.send(sender=VersionRating)


def update_review(self):
    """
        Update the review table from api_engine
        database.
    """

    from .models import StatsLastRecords, VersionReview
    from .api_engine import query_review
    from tools.configfile import update_review_json

    last_recs, created = StatsLastRecords.objects.get_or_create()

    try:
        highest_id, nrating = query_review(last_recs.review_last)
    except Exception as exc:
        raise self.retry(countdown=backoff(self.request.retries), exc=exc)

    if highest_id is None or nrating is None:
        return

    last_recs.review_last = highest_id
    last_recs.save()

    for rt in nrating:

        tool = get_tool(rt.tool_id, rt.tool)
        if tool is None:
            logger.error('Tool does not exist Record {}'.format(str(rt)))
            continue

        obj, created = VersionReview.objects.get_or_create(
            tool=tool,
            platform_name=rt.platform,
            username=rt.user_uuid,
            tool_version=rt.tool_version,
            user_id=rt.user_id)
        if rt.timestamp:
            timestamp = rt.timestamp
            tz = rt.timezone if rt.timezone else settings.TIME_ZONE
            try:
                timestamp = pytz.timezone(tz).localize(timestamp)
            except Exception:
                timestamp = pytz.timezone(settings.TIME_ZONE).localize(timestamp)

            obj.timestamp = timestamp

        obj.language = rt.language
        obj.tool_name = tool.name
        obj.rating = rt.rating
        obj.title = rt.title
        obj.text = rt.text
        obj.save()

    if settings.BUILD_ENV != 'local':
        update_review_json()


def update_feedback(self):
    """
        Update the review table from api_engine
        database.
    """

    from .models import StatsLastRecords, Feedback
    from .api_engine import query_feedback

    last_recs, created = StatsLastRecords.objects.get_or_create()

    try:
        highest_id, nfeedback = query_feedback(last_recs.feedback_last)
    except Exception as exc:
        raise self.retry(countdown=backoff(self.request.retries), exc=exc)

    if highest_id is None or nfeedback is None:
        return

    last_recs.feedback_last = highest_id
    last_recs.save()

    for fb in nfeedback:
        if fb.timestamp:
            timestamp = fb.timestamp
            tz = fb.timezone if fb.timezone else settings.TIME_ZONE
            try:
                timestamp = pytz.timezone(tz).localize(timestamp)
            except Exception:
                timestamp = pytz.timezone(settings.TIME_ZONE).localize(timestamp)

        try:
            Feedback.objects.create(
                timestamp=timestamp,
                title=fb.title,
                text=fb.text,
                user_id=fb.user_id,
                channel=fb.channel,
                channel_version=fb.channel_version,
                platform_name=fb.platform,
                platform_version=fb.platform_version)
        except Exception as e:
            logger.error('Feedback creation failed with exception ({})'.format(str(e)))
            logger.error('Feedback raw data: {}'.format(str(fb)))
            continue


def insert_download(user_uuid,
                    timestamp,
                    tool_name,
                    tool_id,
                    platform,
                    tool_version,
                    file_size,
                    downloaded_via,
                    channel_version):

    from .api_engine import add_download

    dl_dict = {
        'user_uuid': user_uuid,
        'timestamp': timestamp,
        'tool': tool_name,
        'tool_id': tool_id,
        'channel': '{}Web'.format(app.capitalize()),
        'platform': platform,
        'tool_version': tool_version,
        'platform_version': None,
        'download_time': None,
        'downloaded_via': downloaded_via,
        'country': None,
        'city': None,
        'network_type': None,
        'file_size': file_size,
        'network_name': None,
        'channel_version': channel_version,
        'network_country': None,
        'timezone': None,
    }

    try:
        add_download(dl_dict)
    except Exception as exc:
        logger.error('Error inserting download record in api_engine (error = {}) (record={})'.format(str(exc), str(dl_dict)))
        raise errors.DBError('Unable to insert {}\ninto the stats download table: {}'.format(str(dl_dict), str(exc)))


def insert_feedback(user_uuid,
                    timestamp,
                    title,
                    text,
                    user_id,
                    channel_version):

    from .api_engine import add_feedback

    fb_dict = {
        'user_uuid': user_uuid,
        'timestamp': timestamp,
        'channel': '{}Web'.format(app.capitalize()),
        'platform': settings.PLATFORM,
        'platform_version': None,
        'channel_version': channel_version,
        'title': title,
        'text': text,
        'user_id': user_id,
        'timezone': None,
    }

    try:
        add_feedback(fb_dict)
    except Exception as exc:
        logger.error('Error inserting feedback record in api_engine (error = {}) (record={})'.format(str(exc), str(fb_dict)))
        raise errors.DBError('Unable to insert {}\ninto the stats feedback table: {}'.format(str(fb_dict), str(exc)))


def insert_rating(user_uuid,
                  user_id,
                  timestamp,
                  tool_id,
                  tool_name,
                  platform,
                  tool_version,
                  channel_version,
                  rating,
                  title,
                  text,
                  language):

    from .api_engine import add_rating

    rate_dict = {
        'user_uuid': user_uuid,
        'user_id': user_id,
        'timestamp': timestamp,
        'tool_id': tool_id,
        'tool': tool_name,
        'channel': '{}Web'.format(app.capitalize()),
        'platform': platform,
        'tool_version': tool_version,
        'platform_version': None,
        'channel_version': channel_version,
        'rating': rating,
        'title': title,
        'text': text,
        'language': language,
        'timezone': None,
    }

    try:
        add_rating(rate_dict)
    except Exception as exc:
        logger.error('Error inserting rating record in api_engine (error = {}) (record={})'.format(str(exc), str(rate_dict)))
        raise errors.DBError('Unable to insert {}\ninto the stats rating table: {}'.format(str(rate_dict), str(exc)))
