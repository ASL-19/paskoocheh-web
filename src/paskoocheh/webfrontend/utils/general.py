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

u"""webfrontend utilities."""

import logging

from django.conf import settings
from jdatetime import datetime as jdatetime
from ua_parser import user_agent_parser
from preferences.models import GeneralPreference
from paskoocheh.email import Email
from boto3.session import Session
from botocore.client import Config
from botocore.exceptions import ClientError
from django.core.exceptions import FieldError

SUPPORTED_PLATFORM_SLUG_NAMES = (
    'all',
    'android',
    'chrome',
    'firefox',
    'ios',
    'linux',
    'linux32',
    'macos',
    'windows',
    'windows32',
    'windowsphone',
)

logger = logging.getLogger(__name__)

WA_PA_NUMERAL_MAP = {
    '0': '۰',
    '1': '۱',
    '2': '۲',
    '3': '۳',
    '4': '۴',
    '5': '۵',
    '6': '۶',
    '7': '۷',
    '8': '۸',
    '9': '۹',
}

WA_AR_NUMERAL_MAP = {
    '0': '٠',
    '1': '۱',
    '2': '٢',
    '3': '٣',
    '4': '٤',
    '5': '٥',
    '6': '٦',
    '7': '۷',
    '8': '۸',
    '9': '۹',
}


def enforce_required_args(args_dict, *required_arg_names):
    u"""
    Raise a TypeError if any argument name in required_arg_names is missing
    from (or has a value of None in) args_dict. Used to enforce required named
    arguments. There are betters ways of achieving this in Python 3.x.

    Args:
        args_dict (dict): A dictionary of arguments. Should be the return value
            of locals() called before any local variables are defined.
        *required_arg_names (str)

    Returns:
        None (raises TypeError otherwise)
    """
    for arg_name in required_arg_names:
        if args_dict.get(arg_name) is None:
            raise TypeError(
                'Missing a required argument {arg_name}.'.format(
                    arg_name=arg_name
                )
            )

    return None


def get_ua_default_platform_slug_name_os(request):
    u"""Get the request user agent’s Platform name.

    Only returns operating systems, not 'chrome' or 'firefox'

    Args:
        request (WSGIRequest)

    Returns:
        Platform.slug_name value (str)
    """
    if not hasattr(request, 'uap_info'):
        # Default to Android if the request has no user agent for whatever
        # reason
        if ('user-agent' not in request.headers or not request.headers['user-agent']):
            return 'android'

        # Once we know the request has a user agent, parse it with ua_parser
        request.uap_info = (
            user_agent_parser.Parse(request.headers['user-agent'])
        )

    ua_os = request.uap_info['os']['family']

    if ua_os == 'Windows Phone':
        return 'windowsphone'
    elif ua_os == 'Android':
        return 'android'
    elif ua_os == 'iOS':
        return 'ios'
    elif ua_os == 'Linux':
        return 'linux'
    elif ua_os == 'Mac OS X':
        return 'macos'
    elif 'Windows' in ua_os:
        return 'windows'

    return 'android'


def gregorian_datetime_to_jalali_date_string(gregorian_datetime):
    u"""
    Convert a gregorian datetime to a Jalali short date string.

    Args:
        gregorian_datetime (datetime)
    Returns:
        str
    """
    jalali_date_string = replace_wa_numerals_with_pa_numerals(
        jdatetime.fromgregorian(datetime=gregorian_datetime)
        .strftime(u'%Y/%m/%d')
    )

    return jalali_date_string


def image_exists(imagefile):
    u"""
    Tries to determine if an ImageFile exists without needing to open it.

    This is done by checking for the existence of height and width attributes,
    which is a hack that may stop working if Django’s behaviour changes.

    TODO: Use this to consolidate image verification across webfrontend.

    Args:
        imagefile (django.core.files.images.ImageFile)
    Returns:
        unicode
    """

    return (imagefile and hasattr(imagefile, 'height') and hasattr(imagefile, 'width'))


def is_request_user_agent_noop(request):
    u"""
    Determine if a request should be considered noop based on its user agent.

    If the request’s user agent matches any of the patterns in
    NOOP_USER_AGENT_PATTERNS it’s considered noop. Any function that results in
    data being stored (analytics, forms, etc.) should use this function and
    short-circuit (probably returning a 403 error) if it returns True.

    Args:
        request (WSGIRequest)
    Returns:
        bool
    """
    if hasattr(request, 'is_noop'):
        return request.is_noop

    request_user_agent = request.headers.get('user-agent', '')

    if any(noop_regex.match(request_user_agent) for noop_regex in settings.NOOP_USER_AGENT_PATTERNS):
        request.is_noop = True
        return True

    request.is_noop = False
    return False


def replace_wa_numerals_with_pa_numerals(input):
    u"""
    Return input string with all Western Arabic numerals replaced by
    Perso-Arabic numerals.

    See https://en.wikipedia.org/wiki/Eastern_Arabic_numerals

    Args:
        input (str/unicode)
    Returns:
        str
    """
    input = str(input)

    for wa_numeral in WA_PA_NUMERAL_MAP:
        input = input.replace(wa_numeral, WA_PA_NUMERAL_MAP[wa_numeral])

    return input


def replace_wa_numerals_with_ar_numerals(input):
    u"""
    Return input string with all Western Arabic numerals replaced by
    Arabic numerals.

    See https://en.wikipedia.org/wiki/Eastern_Arabic_numerals

    Args:
        input (str/unicode)
    Returns:
        str
    """
    input = str(input)

    for wa_numeral in WA_AR_NUMERAL_MAP:
        input = input.replace(wa_numeral, WA_AR_NUMERAL_MAP[wa_numeral])

    return input


def wrap_with_link(text, href):
    u"""
    Returns provided text wrapped in anchor tag with provided href.

    Args:
        text (str): Text to be wrapped
        href (str): href value of wrapping link
    """
    return '{link_open}{text}{link_close}'.format(
        link_open=(
            u'<a class="pk-g-inline-link inline-link" href="{href}">'.format(
                href=href
            )
        ),
        text=text,
        link_close=u'</a>',
    )


def send_mail(subject, message, from_addr, to_addr):
    """
        Send an email using SES

        Args:
        subject: Subject of email
        message: Body of email
        from_addr: From address
        to_addr: List of To addresses
    """

    email = Email(
        to=to_addr,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    email.subject(subject)
    email.text(message)
    email.send(from_addr=from_addr)


def send_support_notification_email(tool_version, user_email, ticket_message):
    """
        Send notification update to admin support recipient(s) to
        notify about the submission of a new support ticket
        for a tool version

        Args:
        tool_version (tool version object): The tool version on which is the support ticket
        user_email (str): the user email address associated with the user
                    who submitted the support ticket
        ticket_message(str): the ticket message
    """

    general_settings = GeneralPreference.objects.get()
    if not general_settings.from_email:
        msg = 'ERROR: From Email in General Settings (Admin Panel) is not set yet.'
        logger.error(msg)
    elif not general_settings.support_recipient_emails:
        msg = 'ERROR: Support email recipients in General Settings (Admin Panel) are not set yet.'
        logger.error(msg)
    else:
        recipient_list = str(general_settings.support_recipient_emails).split(',')
        if len(recipient_list) > 0:
            logger.info('Sending out support notification email')

            subject = 'New Support Ticket on {} from The Web App'.format(tool_version)
            message = 'Hi Team,\n\nWe have received a new support ticket with the following details:\n'
            message += 'User Email: {}\nAssociated Tool Version: {}\nMessage: "{}"\n\n'.format(
                user_email,
                str(tool_version),
                ticket_message
            )
            message += '--Sent from the Web App.\n'
            from_addr = general_settings.from_email
            to_addr = recipient_list

            send_mail(subject, message, from_addr, to_addr)
        else:
            msg = 'ERROR: Support email recipients in General settings (Admin Panel) should be comma separated values.'
            logger.error(msg)


def send_contact_notification_email(user_email, contact_message, country_code=None):
    """
        Send notification update to admin support recipient(s) to
        notify about the submission of a new contact message

        Args:
        user_email (str): the user email address entered by the user
        contact_message(str): the contact message
        country_code(str): optional
    """

    general_settings = GeneralPreference.objects.get()
    if not general_settings.from_email:
        msg = 'ERROR: From Email in General Settings (Admin Panel) is not set yet.'
        logger.error(msg)
    elif not general_settings.support_recipient_emails:
        msg = 'ERROR: Support email recipients in General Settings (Admin Panel) are not set yet.'
        logger.error(msg)
    else:
        recipient_list = str(general_settings.support_recipient_emails).split(',')
        if len(recipient_list) > 0:
            logger.info('Sending out contact notification email')

            subject = 'New Contact Message from The Web App'
            message = 'Hi Team,\n\nWe have received a new contact message with the following details:\n'
            message += 'User Email: {}\nCountry: {}\nMessage: "{}"\n\n'.format(
                user_email,
                'Not provided' if country_code == '' else country_code,
                contact_message
            )
            message += '--Sent from the Web App.\n'
            from_addr = general_settings.from_email
            to_addr = recipient_list

            send_mail(subject, message, from_addr, to_addr)
        else:
            msg = 'ERROR: Support email recipients in General settings (Admin Panel) should be comma separated values.'
            logger.error(msg)


def get_temp_s3_url(version):
    """
        Get s3 temp url using api credentials and Version Code related to version

        Args:
        version (Version Object): Version object to generate the url based on associated Version Code
    """
    if not version.version_codes:
        return ''

    # Assuming only one Version Code will be there for this Version (non-android platform)
    version_code = version.version_codes.first()
    if not version_code.s3_key:
        return ''

    expiry = 600
    key_id = settings.AWS_ACCESS_KEY_ID
    secret_key = settings.AWS_SECRET_ACCESS_KEY
    session = Session(
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_key
    )
    s3_config = Config(
        signature_version='s3v4',
        s3={'addressing_style': 'path'})
    s3_client = session.client(
        's3',
        settings.S3_REGION,
        config=s3_config)
    try:
        link = s3_client.generate_presigned_url(
            ExpiresIn=expiry,
            ClientMethod='get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': version_code.s3_key.strip('/'),
            }
        )
    except ClientError as error:
        raise FieldError(f"Error generating s3 temp link for version: {str(error)}")
    return link
