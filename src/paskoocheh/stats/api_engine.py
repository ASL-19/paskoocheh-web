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


import logging
from django.db import (
    connections,
    transaction,
)
from paskoocheh.helpers import (
    dictfetchall,
    namedtuplefetchall
)
from preferences.models import Platform

logger = logging.getLogger(__name__)


class RemoteConnectionException(Exception):
    pass


def create_platform_map():
    """
        Create platform map to map name to ids
        NOTE: We also add exception data to the dictionary and
        correct them in local database.

        Returns:
        A dictionary of platforms and their IDs
    """

    platforms = Platform.objects.all()
    platform_map = {}
    for pl in platforms:
        platform_map[pl.name] = pl.id

    # Exceptions
    logger.warning('Added linux_32, linux_64 and mac as platform exceptions')
    platform_map['linux_32'] = platform_map['linux32']
    platform_map['mac'] = platform_map['macos']
    platform_map['linux_64'] = platform_map['linux']

    return platform_map


def get_cursor():
    """
        Return a cursor from api_engine cursor

        Returns:
        A cursor from api_engine
    """

    try:
        cursor = connections['api_engine'].cursor()
    except Exception as exc:
        logger.error('Error connecting to Remote Database ({})'.format(str(exc)))
        raise RemoteConnectionException

    return cursor


@transaction.atomic
def query_table(main_query, maxid_query, prev_id):
    """
        Query the table and return the results for highest
        ID and the main query

        Note: We are not making queries dynamically, which exposes the
        code to vulnerabilities.

        Args:
        main_query: Main query to get the data out of the target table
        maxid_query: Query to get the maximum id of the target table
        prev_id: The last ID in remote database that was queried.
        Returns:
        A tuple: (Highest ID queried, result of the query)
    """

    cursor = get_cursor()
    if cursor is None:
        return None, None

    cursor.execute(maxid_query)
    highest_id = cursor.fetchone()[0]
    cursor.execute(main_query, [prev_id, highest_id])

    return highest_id, namedtuplefetchall(cursor)


def query_download(prev_id):
    """
        Atomically get the highest record for the download table
        and query the number of download per tool-platform.

        Args:
        prev_id: The last ID in remote database that was queried.
        Returns:
        A tuple: (Highest ID queried, result of the query)
    """

    main_query = "SELECT " \
                 "    tool, platform, tool_id, COUNT(*) count " \
                 "FROM " \
                 "    download " \
                 "WHERE " \
                 "    id > %s AND id <= %s " \
                 "GROUP BY " \
                 "    tool, tool_id, platform"

    id_query = "SELECT MAX(id) from download"

    return query_table(main_query, id_query, prev_id)


def query_rating(prev_id):
    """
        Atomically get the highest record for the rating table
        and query the aggregate for AVG rating and number of
        ratings per tool-platform.

        Args:
        prev_id: The last ID in remote database that was queried.
        Returns:
        A tuple: (Highest ID queried, result of the query)
    """

    main_query = "SELECT " \
                 "    tool, platform, tool_id, COUNT(*) count, AVG(rating) star " \
                 "FROM " \
                 "    rating " \
                 "GROUP BY " \
                 "    tool, tool_id, platform"

    id_query = "SELECT MAX(id) from rating"

    return query_table(main_query, id_query, prev_id)


def query_review(prev_id):
    """
        Atomically get the highest record for the rating table
        and query fot the reviews added

        Args:
        prev_id: The last ID in remote database that was queried.
        Returns:
        A tuple: (Highest ID queried, result of the query)
    """

    main_query = "SELECT " \
                 "    tool, tool_id, platform, user_id, user_uuid, tool_version, timestamp, rating, title, text, timezone, language " \
                 "FROM " \
                 "    rating " \
                 "WHERE " \
                 "    id > %s AND id <= %s "

    id_query = "SELECT MAX(id) from rating"

    return query_table(main_query, id_query, prev_id)


def query_feedback(prev_id):
    """
        Atomically get the highest record for the feedback table
        and query fot the feedbacks added

        Args:
        prev_id: The last ID in remote database that was queried.
        Returns:
        A tuple: (Highest ID queried, result of the query)
    """

    main_query = "SELECT " \
                 "    timestamp, timezone, title, text, user_id, channel, channel_version, platform, platform_version " \
                 "FROM " \
                 "    feedback " \
                 "WHERE " \
                 "    id > %s AND id <= %s "

    id_query = "SELECT MAX(id) from feedback"

    return query_table(main_query, id_query, prev_id)


def add_download(dl_dict):

    query = "INSERT INTO " \
            "    download " \
            "        (user_uuid, " \
            "         timestamp, " \
            "         tool, " \
            "         tool_id, " \
            "         channel, " \
            "         platform, " \
            "         tool_version, " \
            "         platform_version, " \
            "         download_time, " \
            "         downloaded_via, " \
            "         country, " \
            "         city, " \
            "         network_type, " \
            "         file_size, " \
            "         network_name, " \
            "         channel_version, " \
            "         network_country, " \
            "         timezone) " \
            "VALUES " \
            "         (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

    cursor = get_cursor()
    if cursor is None:
        raise RemoteConnectionException

    cursor.execute(query, [
        dl_dict['user_uuid'],
        dl_dict['timestamp'],
        dl_dict['tool'],
        dl_dict['tool_id'],
        dl_dict['channel'],
        dl_dict['platform'],
        dl_dict['tool_version'],
        dl_dict['platform_version'],
        dl_dict['download_time'],
        dl_dict['downloaded_via'],
        dl_dict['country'],
        dl_dict['city'],
        dl_dict['network_type'],
        dl_dict['file_size'],
        dl_dict['network_name'],
        dl_dict['channel_version'],
        dl_dict['network_country'],
        dl_dict['timezone']])

    return True


def add_rating(rate_dict):

    query = "INSERT INTO " \
            "    rating " \
            "        (user_uuid," \
            "         user_id," \
            "         tool," \
            "         tool_id," \
            "         platform," \
            "         tool_version," \
            "         channel," \
            "         channel_version," \
            "         platform_version," \
            "         timestamp," \
            "         rating," \
            "         title," \
            "         text," \
            "         language," \
            "         timezone)" \
            "VALUES " \
            "        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

    cursor = get_cursor()
    if cursor is None:
        raise RemoteConnectionException

    cursor.execute(query, [
        rate_dict['user_uuid'],
        rate_dict['user_id'],
        rate_dict['tool'],
        rate_dict['tool_id'],
        rate_dict['platform'],
        rate_dict['tool_version'],
        rate_dict['channel'],
        rate_dict['channel_version'],
        rate_dict['platform_version'],
        rate_dict['timestamp'],
        rate_dict['rating'],
        rate_dict['title'],
        rate_dict['text'],
        rate_dict['language'],
        rate_dict['timezone']])


def add_feedback(fb_dict):

    query = "INSERT INTO " \
            "    feedback " \
            "        (user_uuid," \
            "         timestamp," \
            "         title," \
            "         text," \
            "         user_id," \
            "         channel," \
            "         channel_version," \
            "         platform," \
            "         platform_version," \
            "         timezone)" \
            "VALUES " \
            "         (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

    cursor = get_cursor()
    if cursor is None:
        raise RemoteConnectionException

    cursor.execute(query, [
        fb_dict['user_uuid'],
        fb_dict['timestamp'],
        fb_dict['title'],
        fb_dict['text'],
        fb_dict['user_id'],
        fb_dict['channel'],
        fb_dict['channel_version'],
        fb_dict['platform'],
        fb_dict['platform_version'],
        fb_dict['timezone']])


def get_tools_total_download(start, end):
    """
        Retrieve the total download for all tools in a period

        Args:
        start: Start date (inclusive), if None start from beginning
        end: End date (exclusive), if None get the latest
        Returns:
        A list of tuples: (tool, tool_id, total download)
    """

    params = []

    query = "SELECT " \
            "    tool_id, tool, COUNT(*) count " \
            "FROM " \
            "    download "
    if start is not None:
        query += " WHERE timestamp >= %s "
        params.append(start)
        if end is not None:
            query += "AND timestamp < %s "
            params.append(end)
    else:
        if end is not None:
            query += " WHERE timestamp < %s "
            params.append(end)

    query += "GROUP BY tool, tool_id"

    cursor = get_cursor()
    if cursor is None:
        return None

    cursor.execute(query, params)

    return dictfetchall(cursor)


def get_daily_total_download(start, end):
    """
        Retrieve the daily total download for all tools in a period

        Args:
        start: Start date (inclusive), if None start from beginning
        end: End date (exclusive), if None get the latest
        Returns:
        A list of tuples: (date, total download)
    """

    params = []

    query = "SELECT " \
            "    DATE(timestamp) date, COUNT(*) count " \
            "FROM " \
            "    download "
    if start is not None:
        query += " WHERE timestamp >= %s "
        params.append(start)
        if end is not None:
            query += "AND timestamp < %s "
            params.append(end)
    else:
        if end is not None:
            query += " WHERE timestamp < %s "
            params.append(end)

    query += "GROUP BY date "
    query += "ORDER BY date"

    cursor = get_cursor()
    if cursor is None:
        return None

    cursor.execute(query, params)

    return dictfetchall(cursor)


def get_daily_total_download_per_channel(start, end):
    """
        Retrieve the daily total download for all tools in a period
        for all channels

        Args:
        start: Start date (inclusive), if None start from beginning
        end: End date (exclusive), if None get the latest
        Returns:
        A list of tuples: (date, channel, total download)
    """

    params = []

    query = "SELECT " \
            "    DATE(timestamp) date, channel, COUNT(*) count " \
            "FROM " \
            "    download "
    if start is not None:
        query += " WHERE timestamp >= %s "
        params.append(start)
        if end is not None:
            query += "AND timestamp < %s "
            params.append(end)
    else:
        if end is not None:
            query += " WHERE timestamp < %s "
            params.append(end)

    query += "GROUP BY date, channel "
    query += "ORDER BY date "

    cursor = get_cursor()
    if cursor is None:
        return None

    cursor.execute(query, params)

    return dictfetchall(cursor)


def get_daily_total_download_per_tool(start, end):
    """
        Retrieve the daily total download for all tools in a period
        for all tools

        Args:
        start: Start date (inclusive), if None start from beginning
        end: End date (exclusive), if None get the latest
        Returns:
        A list of tuples: (date, tool, tool_id, total download)
    """

    params = []

    query = "SELECT " \
            "    DATE(timestamp) date, tool, tool_id, COUNT(*) count " \
            "FROM " \
            "    download "
    if start is not None:
        query += " WHERE timestamp >= %s "
        params.append(start)
        if end is not None:
            query += "AND timestamp < %s "
            params.append(end)
    else:
        if end is not None:
            query += " WHERE timestamp < %s "
            params.append(end)

    query += "GROUP BY date, tool, tool_id "
    query += "ORDER BY date"

    cursor = get_cursor()
    if cursor is None:
        return None

    cursor.execute(query, params)

    return dictfetchall(cursor)


def get_daily_total_download_per_platform(start, end):
    """
        Retrieve the daily total download for all tools in a period
        for all platforms

        Args:
        start: Start date (inclusive), if None start from beginning
        end: End date (exclusive), if None get the latest
        Returns:
        A list of tuples: (date, platform, total download)
    """

    params = []

    query = "SELECT " \
            "    DATE(timestamp) date, platform, COUNT(*) count " \
            "FROM " \
            "    download "
    if start is not None:
        query += " WHERE timestamp >= %s "
        params.append(start)
        if end is not None:
            query += "AND timestamp < %s "
            params.append(end)
    else:
        if end is not None:
            query += " WHERE timestamp < %s "
            params.append(end)

    query += "GROUP BY date, platform "
    query += "ORDER BY date"

    cursor = get_cursor()
    if cursor is None:
        return None

    cursor.execute(query, params)

    return dictfetchall(cursor)


def get_monthly_total_download(start, end):
    """
        Retrieve the monthly total download for all tools in a period

        Args:
        start: Start date (inclusive), if None start from beginning
        end: End date (exclusive), if None get the latest
        Returns:
        A list of tuples: (year, month, total download)
    """

    params = []

    query = "SELECT " \
            "    MONTH(timestamp) month, YEAR(timestamp) year, COUNT(*) count " \
            "FROM " \
            "    download "
    if start is not None:
        query += " WHERE timestamp >= %s "
        params.append(start)
        if end is not None:
            query += "AND timestamp < %s "
            params.append(end)
    else:
        if end is not None:
            query += " WHERE timestamp < %s "
            params.append(end)

    query += "GROUP BY year, month "
    query += "ORDER BY year, month"

    cursor = get_cursor()
    if cursor is None:
        return None

    cursor.execute(query, params)

    return dictfetchall(cursor)


def get_monthly_total_download_per_channel(start, end):
    """
        Retrieve the monthly total download for all tools in a period
        for all channels

        Args:
        start: Start date (inclusive), if None start from beginning
        end: End date (exclusive), if None get the latest
        Returns:
        A list of tuples: (year, month, channel, total download)
    """

    params = []

    query = "SELECT " \
            "    MONTH(timestamp) month, YEAR(timestamp) year, channel, COUNT(*) count " \
            "FROM " \
            "    download "
    if start is not None:
        query += " WHERE timestamp >= %s "
        params.append(start)
        if end is not None:
            query += "AND timestamp < %s "
            params.append(end)
    else:
        if end is not None:
            query += " WHERE timestamp < %s "
            params.append(end)

    query += "GROUP BY year, month, channel "
    query += "ORDER BY year, month"

    cursor = get_cursor()
    if cursor is None:
        return None

    cursor.execute(query, params)

    return dictfetchall(cursor)


def get_monthly_total_download_per_tool(start, end):
    """
        Retrieve the monthly total download for all tools in a period
        for all tools

        Args:
        start: Start date (inclusive), if None start from beginning
        end: End date (exclusive), if None get the latest
        Returns:
        A list of tuples: (yaer, month, tool, tool_id, total download)
    """

    params = []

    query = "SELECT " \
            "    MONTH(timestamp) month, YEAR(timestamp) year, tool, tool_id, COUNT(*) count " \
            "FROM " \
            "    download "
    if start is not None:
        query += " WHERE timestamp >= %s "
        params.append(start)
        if end is not None:
            query += "AND timestamp < %s "
            params.append(end)
    else:
        if end is not None:
            query += " WHERE timestamp < %s "
            params.append(end)

    query += "GROUP BY year, month, tool, tool_id "
    query += "ORDER BY year, month"

    cursor = get_cursor()
    if cursor is None:
        return None

    cursor.execute(query, params)

    return dictfetchall(cursor)


def get_monthly_total_download_per_platform(start, end):
    """
        Retrieve the monthly total download for all tools in a period
        for all platforms

        Args:
        start: Start date (inclusive), if None start from beginning
        end: End date (exclusive), if None get the latest
        Returns:
        A list of tuples: (yaer, month, platform, total download)
    """

    params = []

    query = "SELECT " \
            "    MONTH(timestamp) month, YEAR(timestamp) year, platform, COUNT(*) count " \
            "FROM " \
            "    download "
    if start is not None:
        query += " WHERE timestamp >= %s "
        params.append(start)
        if end is not None:
            query += "AND timestamp < %s "
            params.append(end)
    else:
        if end is not None:
            query += " WHERE timestamp < %s "
            params.append(end)

    query += "GROUP BY year, month, platform "
    query += "ORDER BY year, month"

    cursor = get_cursor()
    if cursor is None:
        return None

    cursor.execute(query, params)

    return dictfetchall(cursor)
