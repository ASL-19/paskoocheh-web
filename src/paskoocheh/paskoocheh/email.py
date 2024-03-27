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


import boto3


class Email(object):

    def __init__(self, to, aws_access_key_id, aws_secret_access_key):
        self.to = to
        self._html = None
        self._text = None
        self._format = 'html'
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def html(self, html):
        self._html = html

    def text(self, text):
        self._text = text

    def subject(self, subject):
        self.subject = subject

    def send(self, from_addr):

        if isinstance(self.to, str):
            self.to = [self.to]

        if not from_addr:
            from_addr = 'me@example.com'

        if not self._html and not self._text:
            raise Exception('You must provide a text or html body.')

        if not self._html:
            message = {
                'Subject': {
                    'Data': self.subject
                },
                'Body': {
                    'Text': {
                        'Data': self._text
                    },
                }
            }
        else:
            message = {
                'Subject': {
                    'Data': self.subject
                },
                'Body': {
                    'html': {
                        'Data': self._html
                    },
                    'Text': {
                        'Data': self._text
                    },
                }
            }

        ses = boto3.client(
            service_name='ses',
            region_name='us-east-1',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key)

        destination = {
            'ToAddresses': self.to
        }

        return ses.send_email(
            Source=from_addr,
            Destination=destination,
            Message=message
        )
