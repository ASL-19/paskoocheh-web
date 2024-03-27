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

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    if settings.BUILD_ENV not in ['local', 'ci']:
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        location = settings.MEDIAFILES_LOCATION
        file_overwrite = False


class StaticStorage(S3Boto3Storage):
    if settings.BUILD_ENV not in ['local', 'ci']:
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        location = settings.STATICFILES_LOCATION
        file_overwrite = False


def get_s3_url():
    s3_url = None

    if settings.BUILD_ENV not in ['local', 'ci']:
        if hasattr(settings, 'AWS_S3_CUSTOM_DOMAIN'):
            s3_url = 'https://{s3_domain}'.format(
                s3_domain=settings.AWS_S3_CUSTOM_DOMAIN
            )

    return s3_url
