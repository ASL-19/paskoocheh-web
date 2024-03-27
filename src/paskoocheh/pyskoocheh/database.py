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


""" ActionLog Module
    Holds functions for logging file downloads in DynamoDB
"""
import hashlib
import time as systime
import boto3
from botocore.exceptions import ClientError
from errors import (
    AWSError,
    DBError,
    ValidationError
)
from util import dictfetchall

CLEARED_USER_ID = '-'


# DynamoDB functions
def dynamo_write_rating(user_id, msg, info, table):
    """
        save review in dynamodb

        Args:
        user_id: Telegram User ID
        msg: Review text
        info: A dictionary containing the app name,
        app version and user rating

        Returns:
        True in case of success and False otherwise
    """

    dynamodb = boto3.client('dynamodb')

    item = {
        'user_id': {'S': str(user_id)},
        'date': {'N': str(systime.time())},
        'text': {'S': str(msg)},
        'pkg_name': {'S': str(info['app'])},
        'rating': {'N': str(info['rating'])},
        'version': {'S': str(info['version'])}
    }

    try:
        dynamodb.put_item(
            TableName=table,
            Item=item)
    except ClientError as error:
        raise AWSError('Unable to write to {}: {}'.format(table, str(error)))


def dynamo_write_feedback(user_id, msg, subject, table):
    """
        save feedback in dynamodb

        Args:
        user_id: Telegram User ID
        msg: Feedback message
        subject: Feedback subject line

        Returns:
        True in case of success and False otherwise
    """

    dynamodb = boto3.client('dynamodb')

    item = {
        'user_name': {'S': str(user_id)},
        'feedback_time': {'N': str(systime.time())},
        'message': {'S': str(msg)},
        'subject': {'S': str(subject)},
    }

    try:
        dynamodb.put_item(
            TableName=table,
            Item=item)
    except ClientError as error:
        raise AWSError('Unable to write to {}: {}'.format(table, str(error)))


def dynamo_save_chat_state(user_id, chat_id, state, table, user_info=None, extra_info=None):
    """
        Save the chat request for seeing the report
        or report a new location to the DB

        Args:
        user_id: Telegram User ID
        chat_id: Telegram Chat ID
        state: Different commands the user can run
        user_info: Telegram User Information
        extra_info: Extra Information about the state of the user

        Returns:
        True in case of success and False otherwise
    """

    dynamodb = boto3.client('dynamodb')

    item = {
        'user_id': {'S': str(user_id)},
        'chat_id': {'S': str(chat_id)},
        'timestamp': {'N': str(systime.time())},
        'state': {'N': str(state)},
    }

    if user_info is not None:
        item['user_info'] = {'S': str(user_info)}
    if extra_info is not None:
        item['extra_info'] = {'S': str(extra_info)}

    try:
        dynamodb.put_item(
            TableName=table,
            Item=item)
    except ClientError as error:
        raise AWSError('Unable to write to {}: {}'.format(table, str(error)))


def dynamo_get_chat_state(user_id, chat_id, table):
    """
        Retrieves the state of chat that is saved in the
        DB.

        Args:
        user_id: Telegram User ID
        chat_id: Telegram Chat ID

        Returns:
        Status of the chat or -1 in case of failure, along with the
        extra information saved for the state
    """

    dynamodb = boto3.client('dynamodb')
    try:
        result = dynamodb.get_item(
            TableName=table,
            ConsistentRead=True,
            Key={
                'user_id': {'S': str(user_id)},
                'chat_id': {'S': str(chat_id)},
            }
        )
    except ClientError as error:
        raise AWSError('Unable to read from {}: {}'.format(table, str(error)))

    if len(result['Item']) == 0:
        return None

    inf = None
    if 'extra_info' in result['Item']:
        inf = str(result['Item']['extra_info']['S'])

    return int(result['Item']['state']['N']), inf


def write_rating(rating_data, db_conn, rtime=None):
    """
        save review in db

        Args:
            rating_data: A dictionary that contains the following data:
                user_uuid: User unique identifier
                tool: Tool name
                channel: Channel through which the file is rated
                platfrom: Platform for the tool
                tool_version: Version of the tool rated
                platform_version: Version of the platform for the tool
                channel_version: Version of the channel user is using to rate the app
                rating: The country the network is in
                title: Timezone of the user
                text: ID of the tool rated
                timezone: Timezone of the user
                user_id: ID of the user who rates
                tool_id: ID of the tool rated
            rtime: Time of the rating, if None current time is used
        Returns:
            None
        Raises:
            MYSQLError: MySQL call failed
            ValidationError: Error in configuration
    """

    if rtime is None:
        rtime = systime.time()
    if db_conn is None:
        raise ValidationError('Invalid DB connection')

    user_hash = hashlib.sha512(str(rating_data['user_uuid'])).hexdigest()
    row = [(
        user_hash,
        systime.strftime('%Y-%m-%d %H:%M:%S', systime.gmtime(float(rtime))),
        rating_data['tool'],
        rating_data['channel'],
        rating_data['platform'],
        rating_data['tool_version'],
        rating_data['platform_version'],
        rating_data['channel_version'],
        rating_data['rating'],
        rating_data['title'],
        rating_data['text'],
        rating_data['timezone'],
        rating_data['user_id'],
        rating_data['tool_id']
    )]

    try:
        insert_into_rating(row, db_conn)

    except Exception as exc:
        raise DBError('Unable to insert into rating table: {}'.format(str(exc)))

    return


def write_feedback(feedback_data, db_conn, ftime=None):
    """
        save feedback in DB

        Args:
            feedback_data: A dictionary that contains the following data:
                user_uuid: User unique identifier
                title: Title of the feedback
                text: text of the feedback
                user_id: ID of the user who submitted feedback
                channel: Channel through which the feedback is posted
                channel_version: Version of the channel user is using to submit feedback
                platfrom: Platform of the user submitting feedback
                platform_version: Version of user's platform
                timezone: Timezone of the user
            ftime: Time of the feedback, if None current time is used
        Returns:
            None
        Raises:
            MYSQLError: MySQL call failed
            ValidationError: Error in configuration

    """

    if ftime is None:
        ftime = systime.time()
    if db_conn is None:
        raise ValidationError('Invalid DB connection')

    user_hash = hashlib.sha512(str(feedback_data['user_uuid'])).hexdigest()
    row = [(
        user_hash,
        systime.strftime('%Y-%m-%d %H:%M:%S', systime.gmtime(float(ftime))),
        feedback_data['title'],
        feedback_data['text'],
        feedback_data['user_id'],
        feedback_data['channel'],
        feedback_data['channel_version'],
        feedback_data['platform'],
        feedback_data['platform_version'],
        feedback_data['timezone'],
    )]

    try:
        insert_into_feedback(row, db_conn)

    except Exception as exc:
        raise DBError('Unable to insert into feedback table: {}'.format(str(exc)))

    return


def save_chat_state(state_data, db_conn, mysql, stime=None):
    """
        save chat state with a user in DB

        Args:
            state_data: A dictionary that contains the following data:
                user_uuid: User unique identifier
                chat_id: ID of the telegram chat
                state: Chat state to be saved
                user_info: Telegram user information
                extra_info: Extra information about the state of the chat
            stime: Time the state is stored in the database
        Returns:
            None
        Raises:
            DBError: MySQL call failed
            ValidationError: Error in configuration

    """

    if stime is None:
        stime = systime.time()
    if db_conn is None:
        raise ValidationError('Invalid DB connection')

    user_hash = hashlib.sha512(str(state_data['user_uuid'])).hexdigest()
    chat_hash = hashlib.sha512(str(state_data['chat_id'])).hexdigest()
    if mysql:
        row = [(
            user_hash,
            systime.strftime('%Y-%m-%d %H:%M:%S', systime.gmtime(float(stime))),
            chat_hash,
            state_data['state'],
            state_data['user_info'],
            state_data['extra_info'],
        )]
    else:
        row = [(
            user_hash,
            systime.strftime('%Y-%m-%d %H:%M:%S', systime.gmtime(float(stime))),
            chat_hash,
            state_data['state'],
            state_data['user_info'],
            state_data['extra_info'],
            systime.strftime('%Y-%m-%d %H:%M:%S', systime.gmtime(float(stime))),
            chat_hash,
            state_data['state'],
            state_data['user_info'],
            state_data['extra_info'],
        )]

    try:
        insert_into_state(row, db_conn, mysql)

    except Exception as exc:
        raise DBError('Unable to insert into state table: {}'.format(str(exc)))

    return


def get_chat_state(user_uuid, chat_id, db_conn):
    """
        Retrieves the state of chat that is saved in the DB.

        Args:
            user_id: Telegram User ID
            chat_id: Telegram Chat ID

        Returns:
            Status of the chat or -1 in case of failure, along with the
            extra information saved for the state
    """

    if db_conn is None:
        raise ValidationError('Invalid DB connection')

    user_hash = hashlib.sha512(str(user_uuid)).hexdigest()
    chat_hash = hashlib.sha512(str(chat_id)).hexdigest()

    data = {
        'user_uuid': user_hash,
        'chat_id': chat_hash
    }

    sql_stmt = ('SELECT state, extra_info FROM state ' +
                ' WHERE user_uuid = \'' + data['user_uuid'] + '\'' +
                '   AND chat_id = \'' + data['chat_id'] + '\'')

    try:
        cur = db_conn.cursor()
        cur.execute(sql_stmt)

        row = cur.fetchone()

    except Exception as exc:
        raise DBError('Unable to retrieve state table: {}'.format(str(exc)))

    if row is None:
        return None

    return (row[0], row[1])


def insert_into_download(rows, table, db_conn):
    """
        Insert the given rows of data into database.

        @type row: list of tuples
            List containing tuples corresponding to database entry columns

        @type db_conn: Connection
            A database connection
    """

    if db_conn is None:
        raise ValidationError('Invalid db connection')

    sql_stmt = ('INSERT INTO ' + table +
                ' (user_uuid, timestamp, tool, channel, platform, ' +
                'tool_version, platform_version, download_time, downloaded_via, country, ' +
                'city, network_type, file_size, network_name, channel_version, network_country, ' +
                'timezone, tool_id) ' +
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    db_conn.cursor().executemany(sql_stmt, rows)
    db_conn.commit()


def check_download_exist(data, table, db_conn):
    """
        Check if the record exist in the past 'secs' time
    """

    if db_conn is None:
        raise ValidationError('Invalid db connection')

    sql_stmt = ('SELECT id FROM ' + table +
                ' WHERE user_uuid = \'' + data['user_uuid'] + '\'' +
                '   AND timestamp > \'' + data['timestamp'] + '\'' +
                '   AND tool = \'' + data['tool'] + '\'' +
                '   AND platform = \'' + data['platform'] + '\'')
    if data['channel'] is not None:
        sql_stmt += '   AND channel = \'' + data['channel'] + '\''

    cur = db_conn.cursor()
    cur.execute(sql_stmt)

    return cur.rowcount > 0


def insert_into_rating(rows, db_conn):
    """
        Insert the given rows of data into MySQL database

        @type row: list of tuples
            List containing tuples corresponding to database entry columns

        @type db_conn: Connection
            A database connection
    """

    if db_conn is None:
        raise ValidationError('Invalid db connection')

    sql_stmt = ('INSERT INTO rating ' +
                ' (user_uuid, timestamp, tool, channel, platform, ' +
                'tool_version, platform_version, channel_version, rating, ' +
                'title, text, timezone, user_id, tool_id) ' +
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    db_conn.cursor().executemany(sql_stmt, rows)
    db_conn.commit()


def insert_into_feedback(rows, db_conn):
    """
        Insert the given rows of data into MySQL database

        @type row: list of tuples
            List containing tuples corresponding to database entry columns

        @type db_conn: Connection
            A database connection
    """

    if db_conn is None:
        raise ValidationError('Invalid db connection')

    sql_stmt = ('INSERT INTO feedback ' +
                ' (user_uuid, timestamp, title, text, user_id, channel, ' +
                'channel_version, platform, platform_version, timezone) ' +
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')

    db_conn.cursor().executemany(sql_stmt, rows)
    db_conn.commit()


def insert_into_state(rows, db_conn, mysql):
    """
        Insert the given rows of data into MySQL database

        @type row: list of tuples
            List containing tuples corresponding to database entry columns

        @type db_conn: Connection
            A database connection
    """

    if mysql:
        sql_stmt = ('REPLACE INTO state ' +
                    ' (user_uuid, timestamp, chat_id, state, user_info, extra_info) ' +
                    'VALUES (%s, %s, %s, %s, %s, %s)')
    else:
        sql_stmt = ('INSERT INTO state ' +
                    ' (user_uuid, timestamp, chat_id, state, user_info, extra_info) ' +
                    'VALUES  (%s, %s, %s, %s, %s, %s) ' +
                    'ON CONFLICT (user_uuid, chat_id) DO UPDATE ' +
                    ' SET timestamp = %s, ' +
                    ' chat_id = %s,' +
                    ' state = %s,' +
                    ' user_info = %s, ' +
                    ' extra_info = %s')

    db_conn.cursor().executemany(sql_stmt, rows)
    db_conn.commit()


def insert_into_mailinglist(rows, db_conn):
    """
        Insert the given rows of data into database

        @type row: list of tuples
            List containing tuples corresponding to database entry columns

        @type db_conn: Connection
            A database connection
    """

    sql_stmt = ('INSERT INTO mailinglist ' +
                ' (email, registered_in, user_id, info) ' +
                'VALUES (%s, %s, %s, %s)')

    db_conn.cursor().executemany(sql_stmt, rows)
    db_conn.commit()


def write_download(download_data, db_conn, dtime=None, table=None):
    """ Log action to action_log table for analytics

    Args:
        download_data: A dictionary that contains the following data:
            user_uuid: User unique identifier
            tool: Tool name
            channel: Channel through which the file is downloaded
            platfrom: Platform for the tool
            tool_version: Version of the tool downloaded
            platform_version: Version of the platform for the tool
            download_time: Time taken to download the tool
            downloaded_via: Which link the file is downloaded via
            country: Country of the user downloading the app
            city: City of the user downloading the app
            network_type: Type of network the user is on
            file_size: Size of the file
            network_name: Name of the network the user is on
            channel_version: Version of the channel user is using to download the app
            network_country: The country the network is in
            timezone: Timezone of the user
            tool_id: ID of the tool downloaded
        dtime: Time of the download, if None current time is used
        table: Destination table name
    Returns:
        None
    Raises:
        MYSQLError: MySQL call failed
        ValidationError: Error in configuration
    """

    if dtime is None:
        dtime = systime.time()
    if table is None:
        table = 'download'
    if db_conn is None:
        raise ValidationError('Invalid db connection')

    user_hash = hashlib.sha512(str(download_data['user_uuid'])).hexdigest()
    row = [(
        user_hash,
        systime.strftime('%Y-%m-%d %H:%M:%S', systime.gmtime(float(dtime))),
        download_data['tool'],
        download_data['channel'],
        download_data['platform'],
        download_data['tool_version'],
        download_data['platform_version'],
        download_data['download_time'],
        download_data['downloaded_via'],
        download_data['country'],
        download_data['city'],
        download_data['network_type'],
        download_data['file_size'],
        download_data['network_name'],
        download_data['channel_version'],
        download_data['network_country'],
        download_data['timezone'],
        download_data['tool_id']
    )]

    try:
        insert_into_download(row, table, db_conn)

    except Exception as exc:
        raise DBError('Unable to insert into download table: {}'.format(str(exc)))

    return


def record_exist(user_uuid, tool, platform, channel, db_conn, expiry=85000, table=None):
    """
        Check if a record for the user exist during the past 'expiry'
        time

    Args:
        user_name: user uuid of the record to search
        tool: tool name of the record to search
        platform: platform name of the record to search
        channel: channel name of the record to search in case
            it's none check for all channels
        expiry: seconds to go back for search default to 23 hours
        table: Table in which to search for
    Returns:
        true if found
    Raises:
        MYSQLError: when MySQL call fails
    """

    if table is None:
        table = 'download'
    if db_conn is None:
        raise ValidationError('Invalid db connection')

    user_hash = hashlib.sha512(str(user_uuid)).hexdigest()
    timestamp = systime.time() - expiry
    timestamp = systime.strftime('%Y-%m-%d %H:%M:%S', systime.gmtime(float(timestamp)))

    data = {
        'user_uuid': user_hash,
        'timestamp': timestamp,
        'tool': tool,
        'platform': platform,
        'channel': channel
    }

    try:
        return check_download_exist(data, table, db_conn)

    except Exception as exc:
        raise DBError('Unable to retrieve action log: {}'.format(str(exc)))


def write_email(email_data, db_conn):
    """
        save email in DB

        Args:
            email_data: A dictionary that contains the following data:
                email: email of the user
                registered_in: channel used to subscribe
                user_id: User identifier
                info: Other information about the user
        Returns:
            None
        Raises:
            DBErrorr: DB call failed
            ValidationError: Error in configuration

    """

    if db_conn is None:
        raise ValidationError('Invalid DB connection')
    if email_data['email'] is None:
        raise ValidationError('Email address should not be empty')

    row = [(
        email_data['email'],
        email_data['registered_in'],
        email_data['user_id'],
        email_data['info'],
    )]

    try:
        insert_into_mailinglist(row, db_conn)

    except Exception as exc:
        raise DBError('Unable to insert into mailinglist table: {}'.format(str(exc)))

    return


def write_user(userid, channel, server_id, db_conn):
    """
        save email in DB

        Args:
            userid: user ID
            channel: channel used to subscribe
            server_id: server the user is assigned to
            db_conn: Database connection
        Returns:
            None
        Raises:
            DBErrorr: DB call failed
            ValidationError: Error in configuration

    """

    if db_conn is None:
        raise ValidationError('Invalid DB connection')

    row = [(
        userid,
        channel,
        server_id
    )]

    try:
        insert_into_userdata(row, db_conn)

    except Exception as exc:
        raise DBError('Unable to insert into users table: {}'.format(str(exc)))

    return


def insert_into_userdata(rows, db_conn):
    """
        Insert the given rows of data into database

        @type row: list of tuples
            List containing tuples corresponding to database entry columns

        @type db_conn: Connection
            A database connection
    """

    sql_stmt = ('INSERT INTO users ' +
                ' (userid, channel, server_id) ' +
                'VALUES (%s, %s, %s)')

    db_conn.cursor().executemany(sql_stmt, rows)
    db_conn.commit()


def get_servers(channel, db_conn):
    """
        Retrieves the servers associated with the channel

        Args:
            channel: Channel the server is associated with
            db_conn: Database connection

        Returns:
            list of servers
    """

    if db_conn is None:
        raise ValidationError('Invalid DB connection')

    sql_stmt = ('SELECT outline_servers.id, outline_servers.created, provider, name, cost_per_month, s3_link, count(outline_servers.id) user_count' +
                ' FROM outline_servers JOIN users ON outline_servers.id = users.server_id' +
                ' WHERE user_src = %s' +
                ' GROUP BY outline_servers.id' +
                ' ORDER BY user_count')

    try:
        cur = db_conn.cursor()
        cur.execute(sql_stmt, (channel,))

    except Exception as exc:
        raise DBError('Unable to retrieve outline_servers table: {}'.format(str(exc)))

    servers = dictfetchall(cur)
    if servers is None:
        return None

    return servers


def check_user(userid, db_conn):
    """
        Check if the user exist in the database
    """

    sql_stmt = ('SELECT id FROM users' +
                ' WHERE userid = %s')

    cur = db_conn.cursor()
    cur.execute(sql_stmt, (userid,))

    return cur.rowcount > 0


def insert_into_apps_data(rows, db_conn):
    """
        Insert the given rows of data into database.

        @type row: list of tuples
            List containing tuples corresponding to database entry columns

        @type db_conn: Connection
            A database connection
    """

    if db_conn is None:
        raise ValidationError('Invalid db connection')

    sql_stmt = ("INSERT INTO apps_data " +
                " (id, app_os_name, os, app_name, checksum, " +
                "last_modified, package_name, release_date, size, " +
                "tool_id, version_code, version_number) " +
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" +
                "ON CONFLICT (app_os_name) DO UPDATE " +
                "SET os = %s, " +
                "    app_name = %s, " +
                "    checksum = %s, " +
                "    last_modified = %s, " +
                "    package_name = %s, " +
                "    release_date = %s, " +
                "    size = %s, " +
                "    tool_id = %s, " +
                "    version_code = %s, " +
                "    version_number = %s ")

    db_conn.cursor().executemany(sql_stmt, rows)
    db_conn.commit()


def retrieve_app_data(action_name, current_data, db_conn):
    ''' Given a valid action_name, retrieve the corresponding application data
        and add it to the given current_data dictionary in-place.

        This methods queries the application data table to gain additional
        applicaiton data information.

        @type action_name: str
            A valid action_name of the record provided by DynamoDB.

        @type current_data: dict
            A dictionary of the collect application data thus far.

        @type db_conn: Connection
            A database open connection
    '''

    if db_conn is None:
        raise ValidationError('Invalid db connection')

    with db_conn.cursor() as cur:
        cur.execute('SELECT app_name, os, version_number, size ' +
                    ' FROM apps_data ' +
                    ' WHERE app_os_name=\'' + action_name + '\'')
        retrieved_record = cur.fetchone()
        current_data[action_name] = {
            'app_name': retrieved_record[0],
            'platform': retrieved_record[1],
            'version_number': retrieved_record[2],
            'size': retrieved_record[3]
        }


def psql_get_database_schema(db_conn):
    '''
        Retrieve information about tables and columns from the RDS db.
    '''

    if db_conn is None:
        raise ValidationError('Invalid db connection')

    db_schema = {}
    with db_conn.cursor() as cur:
        cur.execute('SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname=\'public\'')
        rows = cur.fetchall()
        tables = [row[0] for row in rows]

        for table in tables:
            cur.execute('SELECT column_name FROM ' +
                        ' information_schema.columns WHERE ' +
                        '  table_schema=\'public\' ' +
                        '  AND table_name=\'' + table + '\'')
            rows = cur.fetchall()
            db_schema[table] = [row[0] for row in rows]

    return db_schema


def mysql_get_database_schema(db_conn):
    '''
        Retrieve information about tables and columns from the RDS db.
    '''

    if db_conn is None:
        raise ValidationError('Invalid db connection')

    db_schema = {}
    with db_conn.cursor() as cur:
        cur.execute('SHOW TABLES')
        rows = cur.fetchall()
        tables = [row[0] for row in rows]

        for table in tables:
            cur.execute('SELECT `COLUMN_NAME` FROM ' +
                        ' `INFORMATION_SCHEMA`.`COLUMNS` WHERE ' +
                        '  `TABLE_SCHEMA`=\'stats\' ' +
                        '  AND `TABLE_NAME`=\'' + table + '\'')
            rows = cur.fetchall()
            db_schema[table] = [row[0] for row in rows]

    return db_schema


def insert_api_data(request_type, request_type_columns, data, db_conn):
    '''
        Insert the given data into the correct table corresponding to the
        given request_type in an RDS instance.

        @type request_type: str
            The request type of the uploaded file.
        @type data: dict
            Key value pairs of data to be inserted into the table.
    '''

    if db_conn is None:
        raise ValidationError('Invalid db connection')

    data_keys = data.keys()
    data_vals = data.values()

    columns_to_insert = '({})'.format(', '.join(data_keys))
    num_vals_to_insert = '({})'.format(('%s, ' * len(data_keys))[:-2])

    sql_stmt = ('INSERT INTO ' + request_type +
                ' {} '.format(columns_to_insert) +
                'VALUES {}'.format(num_vals_to_insert))

    with db_conn.cursor() as cur:
        cur.execute(sql_stmt, data_vals)
        db_conn.commit()


def log_error_to_rds(record, error, db_conn):
    '''
        Write the given Exception error the an RDS instance

        @type record: dict
            The DynamoDB record that is causing the error.

        @type error: Exception
            An Exception that occurred that will be written to the RDS.

        @type db_conn: Connection
            A database open connection
    '''

    if db_conn is None:
        raise ValidationError('Invalid db connection')

    err_str = ('Error translating DynamoDB record to RDS: ' + str(record))
    err_str += '\n' + str(error)
    time_stamp = systime.strftime('%Y-%m-%d %H:%M:%S', systime.gmtime(systime.time()))
    db_conn.cursor().execute('INSERT INTO trigger_errors ' +
                             ' (timestamp, error_msg) VALUES (%s, %s)',
                             (time_stamp, err_str))
    db_conn.commit()
