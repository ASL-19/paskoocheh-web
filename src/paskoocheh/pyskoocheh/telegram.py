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

""" Telegram Module

    Holds functions for working with Telegram API
"""
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout, TooManyRedirects
from pyskoocheh.errors import AWSError, TelegramError, ValidationError
import pyskoocheh.storage as storage

TELEGRAM_HOSTNAME = "https://api.telegram.org"
TELEGRAM_SEC_PORT = 443
TELEGRAM_METHOD = "POST"
MAX_ITEMS_PER_ROW = 4


def get_file_path(token, file_id):
    """ Send a text message and hides the keyboard for the user.

    Args:
        token: telegram api key
        file_id: file_id for the file to be retrieved
    Returns:
        Telegram API response
    Raises:
        TelegramError: post to api failed
    """
    post_data = {
        "file_id": file_id
    }

    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(post_data)))
    }

    url = make_getfile_url(token)
    try:
        response = requests.post(url, headers=headers, data=json.dumps(post_data))
    except ConnectionError as error:
        raise TelegramError("Error connecting to Telegram API: {}".format(str(error)))
    except HTTPError as error:
        raise TelegramError("Error in POST request to Telegram API: {}".format(str(error)))
    except Timeout as error:
        raise TelegramError("Timeout connecting to Telegram API: {}".format(str(error)))
    except TooManyRedirects as error:
        raise TelegramError("Too many redirects contacting Telegram API: {}".format(str(error)))
    return response


def hide_keyboard(token, chat_id, text):
    """ Send a text message and hides the keyboard for the user.

    Args:
        token: telegram api key
        chat_id: ID of the chat with the user
        text: text to be sent with the link
    Returns:
        Telegram api response
    Raises:
        TelegramError: Error calling Telegram API
    """
    post_data = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {"hide_keyboard": True}
    }

    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(post_data)))
    }

    url = TELEGRAM_HOSTNAME + "/bot" + token + "/sendMessage"
    try:
        response = requests.post(url, headers=headers, data=json.dumps(post_data))
    except ConnectionError as error:
        raise TelegramError("Error connecting to Telegram API: {}".format(str(error)))
    except HTTPError as error:
        raise TelegramError("Error in POST request to Telegram API: {}".format(str(error)))
    except Timeout as error:
        raise TelegramError("Timeout connecting to Telegram API: {}".format(str(error)))
    except TooManyRedirects as error:
        raise TelegramError("Too many redirects contacting Telegram API: {}".format(str(error)))

    if response.status_code >= 400:
        raise TelegramError("Error response from Telegram API:"
                            " {} {}".format(str(response), response.text))

    return response


def make_file_url(token, file_path):
    """ Create a url for getting the file using its path

    Args:
        token: telegram api key
        file_path: file path of the file to be retrieved
    Returns:
        Link (telegram url) to requested file
    """
    return TELEGRAM_HOSTNAME + "/file/bot" + token + "/" + file_path


def make_getfile_url(token):
    """ Create a url for getting the file path from file id

    Args:
        token: telegram api key
    Returns:
        Link (getfile url) to requested file
    """
    return TELEGRAM_HOSTNAME + "/bot" + token + "/getFile"


def make_keyboard(items, items_per_row=0, add_home=""):
    """ Makes a keyboard json out of items list and order them per items_per_row.

    Args:
        items: buttons texts list
        items_per_row: Number of items per row, if not
           specified it uses its own algorithm.
        add_home: if it should add a back to home button
    Returns:
        keyboard object for use in Telegram API
    """
    keyboard = []
    row = []
    count = 0

    if items_per_row > MAX_ITEMS_PER_ROW or items_per_row < 1:
        items_per_row = MAX_ITEMS_PER_ROW

    for item in items:
        row.append(item)
        count += 1
        if count == items_per_row:
            keyboard.append(list(row))
            row = []
            count = 0

    if len(row) != 0:
        keyboard.append(list(row))

    if add_home != "":
        keyboard.append([add_home])

    return keyboard


def send_file(token, chat_id, text, file_bucket, file_key):
    """ Returns a file to the user using the S3 link provided

    Args:
        token: telegram api key
        chat_id: ID of the chat with the user
        text: text to be sent with the link
        file_bucket: bucket of the file in S3
        file_key: key of file to send in S3
    Returns:
        response from Telegram API call
    Raises:
        TelegramError: when Telegram API call fails
    """
    if file_bucket is None or len(file_bucket) == "":
        raise ValidationError("S3 Bucket name is empty")

    if file_key is None or len(file_key) == "":
        raise ValidationError("S3 Key name is empty")

    if text is None or len(text) <= 0:
        raise ValidationError("Text cannot be empty")

    metadata = storage.get_object_metadata(file_bucket, file_key).metadata
    if "file_id" in metadata:
        # send file_id
        file_id = metadata["file_id"]
        _send_document_cached(token, chat_id, file_bucket, file_key, file_id)
    else:
        _send_document_from_s3(token, chat_id, file_bucket, file_key)


def _send_document_cached(token, chat_id, file_bucket, file_key, file_id):
    """
    Send Telegram-cached copy of file
    """
    lookup_file_id = get_file_path(token, file_id).json()
    if lookup_file_id["ok"] and "result" in lookup_file_id:
        post_data = {
            "chat_id": chat_id,
            "document": file_id
        }
        url = TELEGRAM_HOSTNAME + "/bot" + token + "/sendDocument"

        try:
            response = requests.post(url, data=post_data)
        except ConnectionError as error:
            raise TelegramError("Error connecting to Telegram API: {}".format(str(error)))
        except HTTPError as error:
            raise TelegramError("Error in POST request to Telegram API: {}".format(str(error)))
        except Timeout as error:
            raise TelegramError("Timeout connecting to Telegram API: {}".format(str(error)))

        if response.status_code >= 400:
            raise TelegramError("Error response from Telegram API:"
                                " {} {}".format(str(response), response.text))
        return response
    else:
        # cache miss
        _send_document_from_s3(token, chat_id, file_bucket, file_key)


def _send_document_from_s3(token, chat_id, file_bucket, file_key):    # noqa: C901
    """
    Send document directly to Telegram user
    """
    try:
        file_to_send = storage.get_binary_contents(file_bucket, file_key)
    except ConnectionError as error:
        raise TelegramError("Error connecting to Telegram API: {}".format(str(error)))
    except HTTPError as error:
        raise TelegramError("Error in GET request to Telegram API: {}".format(str(error)))
    except Timeout as error:
        raise TelegramError("Timeout connecting to Telegram API: {}".format(str(error)))
    except IOError as error:
        raise TelegramError("Error reading file: {}".format(str(error)))

    post_data = {
        "chat_id": chat_id
    }
    filename = file_key.split("/")[-1]
    file_data = {
        "document": (filename, file_to_send["Body"])
    }
    url = TELEGRAM_HOSTNAME + "/bot" + token + "/sendDocument"

    try:
        response = requests.post(url, files=file_data, data=post_data)
    except ConnectionError as error:
        raise TelegramError("Error connecting to Telegram API: {}".format(str(error)))
    except HTTPError as error:
        raise TelegramError("Error in POST request to Telegram API: {}".format(str(error)))
    except Timeout as error:
        raise TelegramError("Timeout connecting to Telegram API: {}".format(str(error)))

    if response.status_code >= 400:
        raise TelegramError("Error response from Telegram API:"
                            " {} {}".format(str(response), response.text))

    try:
        data = response.json()
    except ValueError as error:
        raise TelegramError("Error in response: {} - {}".format(str(response.text), str(error)))

    if data["ok"] and "result" in data:
        storage.put_object_metadata(file_bucket, file_key, "file_id",
                                    data["result"]["document"]["file_id"])
    return response


def send_keyboard(token, chat_id, text, keyboard=[], one_time=True, resize=True, inline=False):
    """ Returns a message with keyboard to the user

    Args:
        token: telegram api key
        chat_id: ID of the chat with the user
        text: text to be sent with the link
        keyboard: a compiled keyboard to be sent to the user
        one_time: if one_time_keyboard should be set
        resize: if resize_keyboard should be set
    Returns:
        Telegram API post response
    Raises:
        TelegramError: text is empty or error calling Telegram API
    """
    if text is None or len(text) <= 0:
        raise ValidationError("Text cannot be empty")

    post_data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    if len(keyboard) == 0:
        keyboard = make_keyboard([], 1)

    if inline:
        post_data["reply_markup"] = {
            "inline_keyboard": keyboard,
        }
    else:
        post_data["reply_markup"] = {
            "keyboard": keyboard,
            "one_time_keyboard": one_time,
            "resize_keyboard": resize
        }

    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(post_data)))
    }

    url = TELEGRAM_HOSTNAME + "/bot" + token + "/sendMessage"
    try:
        response = requests.post(url, headers=headers, data=json.dumps(post_data))
    except ConnectionError as error:
        raise TelegramError("Error connecting to Telegram API: {}".format(str(error)))
    except HTTPError as error:
        raise TelegramError("Error in POST request to Telegram API: {}".format(str(error)))
    except Timeout as error:
        raise TelegramError("Timeout connecting to Telegram API: {}".format(str(error)))

    if response.status_code >= 400:
        raise TelegramError("Error response from Telegram API:"
                            " {} {}".format(str(response), response.text))

    return response


def send_message(token, chat_id, text, keyboard=[], parse=None):
    """ Returns a text message to the user

    Args:
        token: telegram api key
        chat_id: ID of the chat with the user
        text: text to be sent with the link
        keyboard: a compiled keyboard to be sent to the user
    Returns:
        Telegram response object
    Raises:
        TelegramError: Telegram API call failed
    """
    if text is None or len(text) <= 0:
        raise ValidationError("Text cannot be empty")

    post_data = {
        "chat_id": chat_id,
        "text": text
    }

    if parse == 'HTML':
        post_data['parse_mode'] = 'HTML'
    elif parse == 'MARKDOWN':
        post_data['parse_mode'] = 'Markdown'

    if len(keyboard) == 0:
        keyboard = make_keyboard([], 1)

    post_data["reply_markup"] = {
        "keyboard": keyboard,
        "one_time_keyboard": False,
        "resize_keyboard": True
    }

    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps(post_data)))
    }

    url = TELEGRAM_HOSTNAME + "/bot" + token + "/sendMessage"
    try:
        response = requests.post(url, headers=headers, data=json.dumps(post_data))
    except ConnectionError as error:
        raise TelegramError("Error connecting to Telegram API: {}".format(str(error)))
    except HTTPError as error:
        raise TelegramError("Error in POST request to Telegram API: {}".format(str(error)))
    except Timeout as error:
        raise TelegramError("Timeout connecting to Telegram API: {}".format(str(error)))

    if response.status_code >= 400:
        raise TelegramError("Error response from Telegram API:"
                            " {} {}".format(str(response), response.text))

    return response


def save_request(chat_id, msg_id, user_name, event, table_name="MajlisMonitorBot"):
    """ Save a telegram request to dynamodb

    Args:
        chat_id: telegram chat id from api
        msg_id: telegram msg id from api
        user_name: name of telegram user
        event: event that triggered lambda call
        context: context of lambda call
        table_name: optional table name (default="MajlisMonitorBot")
    Returns:
        response object from put_item call
    Raises:
        AWSError: db call failed
    """
    timestr = datetime.now().strftime("%Y%m%d-%H:%M:%S.%f.msg")
    message = str(chat_id) + str(msg_id) + "-" + str(user_name)
    record = {
        "datetime": {
            "S": timestr
        },
        "message_id": {
            "S": message
        },
        "request": {
            "S": str(event)
        },
    }
    dynamodb = boto3.client("dynamodb")
    try:
        response = dynamodb.put_item(TableName=table_name, Item=record)
    except ClientError as error:
        raise AWSError("Problem writing to DB {} ({})".format(table_name, str(error)))
    return response


def send_photo(token, chat_id, photo, photoname, caption=None, keyboard=[], inline=False):
    """ Returns a photo to the user

    Args:
        token: telegram api key
        chat_id: ID of the chat with the user
        photo: photo binary to be sent to the user
        keyboard: a compiled keyboard to be sent to the user
    Returns:
        Telegram response object
    Raises:
        TelegramError: Telegram API call failed
    """
    if photo is None or len(photo) <= 0:
        raise ValidationError("Photo cannot be empty")

    post_data = {
        "chat_id": chat_id,
        "parse_mode": "Markdown",
        "caption": caption
    }

    if keyboard:
        if inline:
            post_data["reply_markup"] = {
                "inline_keyboard": keyboard,
            }
        else:
            post_data["reply_markup"] = {
                "keyboard": keyboard,
                "one_time_keyboard": True,
                "resize_keyboard": True
            }

    url = TELEGRAM_HOSTNAME + "/bot" + token + "/sendPhoto"

    try:
        if photoname is None:
            post_data["photo"] = photo

            headers = {
                "Content-Type": "application/json",
                "Content-Length": str(len(json.dumps(post_data)))
            }

            response = requests.post(url, data=json.dumps(post_data), headers=headers)

        else:
            photo_data = {
                "photo": (photoname, photo)
            }
            response = requests.post(url, files=photo_data, data=post_data)

    except ConnectionError as error:
        raise TelegramError("Error connecting to Telegram API: {}".format(str(error)))
    except HTTPError as error:
        raise TelegramError("Error in POST request to Telegram API: {}".format(str(error)))
    except Timeout as error:
        raise TelegramError("Timeout connecting to Telegram API: {}".format(str(error)))

    if response.status_code >= 400:
        raise TelegramError("Error response from Telegram API:"
                            " {} {}".format(str(response), response.text))
    return response


def send_inlinequery_answer(token, response):
    """ Returns a text message to the user

    Args:
        token: telegram api key
        chat_id: ID of the chat with the user
        text: text to be sent with the link
        keyboard: a compiled keyboard to be sent to the user
    Returns:
        Telegram response object
    Raises:
        TelegramError: Telegram API call failed
    """

    if response is None or len(response) <= 0:
        raise ValidationError("Response cannot be empty")

    post_data = {
        "inline_query_id": response['inline_query_id'],
        "results": response['results'],
    }

    if "cache_time" in response:
        post_data["cache_time"] = response["cache_time"]

    if "switch_pm_text" in response:
        post_data["switch_pm_text"] = response["switch_pm_text"]

    if "switch_pm_parameter" in response:
        post_data["switch_pm_parameter"] = response["switch_pm_parameter"]

    headers = {
        "Content-Type": "application/json",
        "Content-Length": len(json.dumps(post_data))
    }

    url = TELEGRAM_HOSTNAME + "/bot" + token + "/answerInlineQuery"
    try:
        response = requests.post(url, headers=headers, data=json.dumps(post_data))
    except ConnectionError as error:
        raise TelegramError("Error connecting to Telegram API: {}".format(str(error)))
    except HTTPError as error:
        raise TelegramError("Error in POST request to Telegram API: {}".format(str(error)))
    except Timeout as error:
        raise TelegramError("Timeout connecting to Telegram API: {}".format(str(error)))

    if response.status_code >= 400:
        raise TelegramError("Error response from Telegram API:"
                            " {} {}".format(str(response), response.text))

    return response


def edit_message_reply_markup(token, message_id, reply_markup, chat_id=None):
    """
        Edit reply markup of the messages sent

    Args:
        inline_message_id: ID of the inline_message to be edited
        reply_markup: the replacement reply markup
    Returns:
        Telegram response object
    Raises:
        TelegramError: Telegram API call failed
    """

    if not message_id:
        raise ValidationError("inline_message_id cannot be empty")

    if not reply_markup:
        raise ValidationError("reply_markup cannot be empty")

    post_data = {
        "reply_markup": reply_markup
    }

    if chat_id:
        post_data["message_id"] = message_id
        post_data["chat_id"] = chat_id
    else:
        post_data["inline_message_id"] = message_id

    headers = {
        "Content-Type": "application/json",
        "Content-Length": len(json.dumps(post_data))
    }

    url = TELEGRAM_HOSTNAME + "/bot" + token + "/editMessageReplyMarkup"
    try:
        response = requests.post(url, headers=headers, data=json.dumps(post_data))
    except ConnectionError as error:
        raise TelegramError("Error connecting to Telegram API: {}".format(str(error)))
    except HTTPError as error:
        raise TelegramError("Error in POST request to Telegram API: {}".format(str(error)))
    except Timeout as error:
        raise TelegramError("Timeout connecting to Telegram API: {}".format(str(error)))

    if response.status_code >= 400:
        raise TelegramError("Error response from Telegram API:"
                            " {} {}".format(str(response), response.text))

    return response


def send_answer_callbackquery(token, message_id, text, show_alert):
    """
        Send Answer to Callback Query

    Args:
        message_id: ID of the callback_query to be answered
        text: text to show to the user
        show_alert: if client should show an alert
    Returns:
        Telegram response object
    Raises:
        TelegramError: Telegram API call failed
    """

    if not message_id:
        raise ValidationError("inline_message_id cannot be empty")

    post_data = {
        "callback_query_id": message_id,
    }

    if text:
        post_data["text"] = text

    if show_alert:
        post_data["show_alert"] = show_alert

    headers = {
        "Content-Type": "application/json",
        "Content-Length": len(json.dumps(post_data))
    }

    url = TELEGRAM_HOSTNAME + "/bot" + token + "/answerCallbackQuery"
    try:
        response = requests.post(url, headers=headers, data=json.dumps(post_data))
    except ConnectionError as error:
        raise TelegramError("Error connecting to Telegram API: {}".format(str(error)))
    except HTTPError as error:
        raise TelegramError("Error in POST request to Telegram API: {}".format(str(error)))
    except Timeout as error:
        raise TelegramError("Timeout connecting to Telegram API: {}".format(str(error)))

    if response.status_code >= 400:
        raise TelegramError("Error response from Telegram API:"
                            " {} {}".format(str(response), response.text))

    return response
