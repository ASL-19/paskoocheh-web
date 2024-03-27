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
logger = logging.getLogger()


class ObjectCreationFailed(Exception):
    pass


class TelegramMessage(object):

    def __init__(self, event, lang):    # noqa: C901

        self.lang = lang
        self.command = ''
        self.command_arg = ''

        if 'message' in event['Input']:
            self.type = 'MESSAGE'
            message = event['Input']['message']
            try:
                self.msg_date = message['date']
                self.id = int(message['message_id'])
                self.chat_id = int(message['chat']['id'])
                if 'from' in message:
                    if 'username' in message['from']:
                        self.user_id = str(message['from']['username'])
                    else:
                        self.user_id = str(message['from']['id'])
                    self.user_info = str(message['from'])
                else:
                    self.user_id = u''
                    self.user_info = u''

                if 'text' in message:
                    self.body = message['text']
                    self.bodytype = 'TEXT'
                elif 'document' in message:
                    self.body = message['document']['file_id']
                    self.bodytype = 'DOCUMENT'
                    self.bodymime = message['document']['mime_type']
                else:
                    self.body = ''
                    self.bodytype = 'UNKNOWN'

            except Exception as exc:
                logger.error(str(exc))
                raise ObjectCreationFailed

        elif 'inline_query' in event['Input']:
            self.type = 'INLINE'
            inline_query = event['Input']['inline_query']
            try:
                self.id = inline_query['id']
                self.chat_id = inline_query['from']['id']
                self.user_id = inline_query['from']['username']
                self.body = inline_query['query']
                self.is_bot = inline_query['from']['is_bot']

            except Exception:
                raise ObjectCreationFailed

        elif 'edited_message' in event['Input']:
            self.type = 'MESSAGE'
            message = event['Input']['edited_message']
            try:
                self.msg_date = message['edit_date']
                self.id = int(message['message_id'])
                self.chat_id = int(message['chat']['id'])
                if 'from' in message:
                    if 'username' in message['from']:
                        self.user_id = str(message['from']['username'])
                    else:
                        self.user_id = str(message['from']['id'])
                    self.user_info = str(message['from'])
                else:
                    self.user_id = u''
                    self.user_info = u''

                self.body = message['text']

            except Exception as exc:
                logger.error(str(exc))
                raise ObjectCreationFailed

        elif 'inline_query' in event['Input']:
            self.type = 'INLINE'
            inline_query = event['Input']['inline_query']
            try:
                self.id = inline_query['id']
                self.chat_id = inline_query['from']['id']
                self.user_id = inline_query['from']['username']
                self.body = inline_query['query']
                self.is_bot = inline_query['from']['is_bot']

            except Exception:
                raise ObjectCreationFailed

        elif 'callback_query' in event['Input']:
            self.type = 'CALLBACK'
            callback_query = event['Input']['callback_query']
            try:
                self.id = callback_query['id']
                if 'message' in callback_query and 'chat' in callback_query['message']:
                    self.chat_id = callback_query['message']['chat']['id']
                else:
                    self.chat_id = callback_query['from']['id']

                if 'message' in callback_query:
                    self.msg_id = callback_query['message']['message_id']
                    self.inline = False
                else:
                    self.msg_id = callback_query['inline_message_id']
                    self.inline = True

                if 'username' in callback_query['from']:
                    self.user_id = callback_query['from']['username']
                else:
                    self.user_id = callback_query['from']['id']

                self.firstname = callback_query['from']['first_name']
                self.body = callback_query['data']

            except Exception:
                raise ObjectCreationFailed

        else:
            logger.error('Undefined message type!')
            raise ObjectCreationFailed

        if self.body[0] == '/':
            self.command = self.body[1:]
            cmd = self.command.split(' ', 1)
            if len(cmd) > 1:
                self.command = str(cmd[0])
                self.command_arg = str(cmd[1])
            self.command = self.command.lower()
