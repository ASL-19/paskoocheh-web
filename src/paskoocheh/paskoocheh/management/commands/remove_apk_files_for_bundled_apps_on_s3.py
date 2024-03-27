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
import boto3

from botocore.exceptions import ClientError
from django.conf import settings
from django.core.management.base import BaseCommand

from paskoocheh.s3 import iterate_s3_objects
from tools.models import Version

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Removes APK files and their respective ASC files from S3 for each bundled Android app (zipped).
    """

    help = 'Removes APK files and their respective ASC files from S3 for each bundled Android app (zipped).'

    def handle(self, *args, **options):

        android_apps = Version.objects \
            .filter(supported_os__slug_name='android') \
            .filter(is_bundled_app=True) \
            .select_related('tool') \
            .order_by('tool__name') \
            .all()

        s3 = boto3.resource(
            's3',
            region_name=settings.S3_REGION,
            config=boto3.session.Config(signature_version='s3v4'),
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        s3client = boto3.client('s3')

        count = len(android_apps)
        self.stdout.write(f'There are currently `{count}` bundled Android apps in the database')

        if count > 0:

            keys = list()
            reclaimed_space = 0

            for i, app in enumerate(android_apps, start=1):
                appname = app.tool.get_app_name()

                self.stdout.write(f'[{i}] {app.tool.name}')

                try:
                    # There are currently two locations for apk/asc files:
                    # [1] ANDROID_TOOLS_PREFIX
                    # [2] TOOLS_PATH

                    if app.s3_key == '' or app.s3_key is None:  # edge case
                        tools_prefix = f'{settings.ANDROID_TOOLS_PREFIX_TEMPLATE.format(appname=appname)}'
                    else:
                        tools_prefix = app.s3_key.split('-')[0].strip('/')

                    keys.extend(iterate_s3_objects(s3client, settings.AWS_STORAGE_BUCKET_NAME, tools_prefix))

                    uploads_prefix = tools_prefix.replace(
                        f'{settings.TOOLS_PREFIX}',
                        f'{settings.MEDIA_PREFIX}{settings.TOOLS_PATH}').strip('/')
                    keys.extend(iterate_s3_objects(s3client, settings.AWS_STORAGE_BUCKET_NAME, uploads_prefix))

                    for j, key in enumerate(keys, start=1):
                        extension = key.split('.')[-1].lower()

                        # Skip any non-targeted files or any split files (APKs)
                        if extension not in ['apk', 'asc', 'zip'] or f'/{settings.SPLITS_PATH}' in key:
                            self.stdout.write(f'  [{j}] Skipping "{key}"')
                            continue

                        if '.zip' in key or '.zip.asc' in key:
                            self.stdout.write(f'  [{j}] Keeping "{key}"')
                        else:
                            self.stdout.write(f'  [{j}] Deleting "{key}"')
                            response = s3client.head_object(
                                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                                Key=key)

                            # Delete the file, if it exists
                            s3.Object(settings.AWS_STORAGE_BUCKET_NAME, key).delete()
                            self.stdout.write('\tDONE!')
                            reclaimed_space += int(response['ContentLength'])

                    # Clear the keys (files) list
                    keys.clear()

                except ClientError as error:
                    self.stdout.write('S3 object deletion failed with error: ' + error.message)

            # Calculate total reclaimed space in the s3 bucket
            reclaimed_space_mb = round(reclaimed_space / 1024 / 1024)
            self.stdout.write(f'\n\nS3 Total Reclaimed Space : {reclaimed_space_mb} MB')

        else:
            self.stdout.write('There are no bundled Android apps at this time.')
