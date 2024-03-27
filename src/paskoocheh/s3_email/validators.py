# -*- coding: utf-8 -*-
# Paskoocheh - A tool marketplace for the Iranian
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
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.conf import settings
from boto3.session import Session


def validate_buck(buck):
    direc = ''
    session = Session(region_name=settings.S3_REGION,
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')
    if '/' in buck:
        direc = buck[buck.index('/') + 1:].replace(' ', '')
        buck = buck[:buck.index('/')]
        if not direc[-1] == '/':
            direc += '/'
    if not s3.Bucket(buck) in s3.buckets.all():
        raise ValidationError(
            _('%(value)s is not a valid bucket'),
            params={'value': buck},
        )
        return
    try:
        # testing if bucket is accessible
        for obj in s3.Bucket(buck).objects.all():
            break
    except Exception as exc:
        raise ValidationError(
            _('%(value)s is not accessible %(error)'),
            params={'value': buck, 'error': str(exc)},
        )
        return
