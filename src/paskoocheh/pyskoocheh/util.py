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


""" Farsi helper Module

    Holds helper functions for languages
"""
import re
import time
import datetime
import jdatetime
import requests
from requests.exceptions import HTTPError
from collections import namedtuple
from dateutil.relativedelta import relativedelta


def read_file_from_url(url):
    """ Reads a binary file from the given url
    """
    try:
        file_content = requests.get(url).content

    except Exception as exc:
        raise HTTPError(str(exc))

    return file_content


def change_digits(input, lang, convert_dec_point=False):
    """ Converts the digits inside a string to
        their Farsi or Arabic equivalents

    Args:
        input: input unicode string
        lang: language to convert to
    Returns:
        "input" string with digits converted
    """
    numbers = {}
    numbers["en"] = u'1234567890.'
    numbers["fa"] = u'۱۲۳۴۵۶۷۸۹۰\u066B'
    numbers["ar"] = u'١٢٣٤٥٦٧٨٩٠\u066B'

    if not convert_dec_point:
        numbers["en"] = numbers["en"][:-1]
        numbers["fa"] = numbers["fa"][:-1]
        numbers["ar"] = numbers["ar"][:-1]

    if lang != "fa" and lang != "ar":
        return input

    def _sub(match_object):
        return numbers[lang][numbers["en"].find(match_object.group(0))]

    def _sub_cb(match_object):
        return _sub(match_object)

    regexp = u"(%s)" % u"|".join(numbers["en"])

    return re.sub(regexp, _sub_cb, input)


def convert_to_multi_dates(input_date):     # noqa: C901
    res = {}
    if input_date > 0:
        localdate = time.localtime(input_date)
        res = {}
        res["gdate"] = time.strftime("%Y-%m-%d %H:%M:%S", localdate)
        res["gshortdate"] = time.strftime("%Y-%m-%d", localdate)
        res["jdate"] = change_digits(jdatetime.datetime.fromtimestamp(input_date).strftime("%aء %-d %b %Y %H:%M:%S"), "fa")
        res["jshortdate"] = change_digits(jdatetime.datetime.fromtimestamp(input_date).strftime("%Y/%-m/%-d"), "fa")

        diff = relativedelta(datetime.datetime.now(), datetime.datetime.fromtimestamp(input_date))
        if diff.years > 0:
            if diff.years > 1:
                res["dgdate"] = u"{} years ago".format(diff.years)
                res["djdate"] = change_digits(u"{} سال پیش".format(diff.years), "fa")
            else:
                res["dgdate"] = u"a year ago"
                res["djdate"] = u"یک سال پیش"
        elif diff.months > 0:
            if diff.months > 1:
                res["dgdate"] = "{} months ago".format(diff.months)
                res["djdate"] = change_digits(u"{} ماه پیش".format(diff.months), "fa")
            else:
                res["dgdate"] = u"a month ago"
                res["djdate"] = u"یک ماه پیش"
        elif diff.days > 0:
            if diff.days > 1:
                res["dgdate"] = u"{} days ago".format(diff.days)
                res["djdate"] = change_digits(u"{} روز پیش".format(diff.days), "fa")
            else:
                res["dgdate"] = "a day ago"
                res["djdate"] = u"یک روز پیش"
        elif diff.hours > 0:
            if diff.hours > 1:
                res["dgdate"] = u"{} hours ago".format(diff.hours)
                res["djdate"] = change_digits(u"{} ساعت پیش".format(diff.hours), "fa")
            else:
                res["dgdate"] = "an hour ago"
                res["djdate"] = u"یک ساعت پیش"
        elif diff.minutes > 0:
            if diff.minutes > 1:
                res["dgdate"] = u"{} minutes ago".format(diff.minutes)
                res["djdate"] = change_digits(u"{} دقیقه پیش".format(diff.minutes), "fa")
            else:
                res["dgdate"] = u"a minute ago"
                res["djdate"] = u"یک دقیقه پیش"
        elif diff.seconds > 0:
            if diff.seconds > 1:
                res["dgdate"] = u"{} seconds ago".format(diff.seconds)
                res["djdate"] = change_digits(u"{} ثانیه پیش".format(diff.seconds), "fa")
            else:
                res["dgdate"] = u"a second ago"
                res["djdate"] = u"یک ثانیه پیش"
        else:
            res["dgdate"] = u"right now"
            res["djdate"] = u"همین الان"

    return res


def email_format(email):
    if email is None:
        return False

    emailre = re.compile(r'[^@]+@[^@]+\.[^@]+')
    return emailre.match(email)


def dictfetchall(cursor):
    """
        Return all rows from a cursor as a namedtuple

        Args,
        cursor: Connection cursor returned by execute function

        Returns:
        A namedtuple of the results

    """
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row)._asdict() for row in cursor.fetchall()]


def namedtuplefetchall(cursor):
    """
        Return all rows from a cursor as a namedtuple

        Args,
        cursor: Connection cursor returned by execute function

        Returns:
        A namedtuple of the results

    """
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def namedtuplefetchone(cursor):
    """
        Return one row from a cursor as a namedtuple

        Args,
        cursor: Connection cursor returned by execute function

        Returns:
        A namedtuple of the result

    """
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return nt_result(*cursor.fetchone())
