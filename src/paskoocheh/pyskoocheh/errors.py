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

""" Holds local library error types """


class PyskoochehException(Exception):
    """ Base class for exceptions in Pyskoocheh """

    def __init__(self, value):
        """ Set value of error message """
        super(PyskoochehException, self).__init__()
        self.value = value

    def __str__(self):
        """ Output representation of error """
        return repr(self.value)


class AWSError(PyskoochehException):
    """ AWS API Error Wrapper """


class FeedbackError(PyskoochehException):
    """ Feedback Error Wrapper """


class TelegramError(PyskoochehException):
    """ Telegram Error Wrapper """


class ValidationError(PyskoochehException):
    """ Validation Error Wrapper """


class HTTPError(PyskoochehException):
    """ HTTP Error on Requests """


class DBError(PyskoochehException):
    """ DB Errors """
