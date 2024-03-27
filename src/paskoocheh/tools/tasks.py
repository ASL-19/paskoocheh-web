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


from __future__ import absolute_import, unicode_literals
import boto3
import logging
from django.conf import settings
from django.core.files.base import ContentFile


logger = logging.getLogger('tools')


def update_json_config():

    if settings.BUILD_ENV != 'local':

        from tools.configfile import update_config_json

        update_config_json()


def update_faq(instanceid):

    if settings.BUILD_ENV != 'local':

        from tools.configfile import (
            update_config_json,
            # update_faqs_telegraph,
        )

        # update_faqs_telegraph(instanceid)
        update_config_json()


def update_guide(instanceid):

    if settings.BUILD_ENV != 'local':

        from tools.configfile import (
            update_config_json,
            # update_guides_telegraph,
        )

        # update_guides_telegraph(instanceid)
        update_config_json()


def upload_file_to_s3(instanceid):
    from tools.models import VersionCode
    from tools.configfile import update_config_json

    boto3.set_stream_logger('boto3.resources', logging.WARNING)

    try:
        instance = VersionCode.objects.get(pk=instanceid)
    except Exception as exc:
        logger.error(f"ERROR: Unable to get the Version Code with pk={instanceid} (error={exc})")
        return

    extension = instance.uploaded_file.name.split('.')[-1].lower()
    has_splits = instance.version.is_bundled_app

    # The Updater (tools.updater) has an intermediate version save() operation for bundled apps
    # to temporarily save the base apk before bundling all version splits + that base apk
    # into a zip file so to optimize the performance of the Updater, this s3 upload shall not
    # go through except for normal apps with apk extension or bundled apps with zip extension
    if (has_splits is True and extension == 'apk'):
        return

    file_exists = (
        instance.uploaded_file and
        instance.s3_key and
        instance.uploaded_file.storage.exists(instance.uploaded_file.name)
    )

    if file_exists:
        if extension == 'zip':
            content_type = 'application/zip'
        elif extension == 'apk':
            content_type = 'application/vnd.android.package-archive'

        if (instance.uploaded_file.name.endswith('.tar.gz') or
                instance.uploaded_file.name.endswith('.tar.xz') or
                instance.uploaded_file.name.endswith('.tar.bz2')):
            content_type = 'application/x-tar'
        else:
            content_type = 'binary/octet-stream'

        s3_res = boto3.resource(
            's3',
            region_name=settings.S3_REGION,
            config=boto3.session.Config(signature_version='s3v4'),
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        logger.info(f"[INFO] (Task) Writing uploaded file ({instance.version.tool.name}) to s3: {settings.AWS_STORAGE_BUCKET_NAME}{instance.s3_key}")
        s3_res.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
            ContentType=content_type,
            StorageClass='REDUCED_REDUNDANCY',
            Key=instance.s3_key.strip('/'),
            Body=instance.uploaded_file.read())

        sig_file_name = instance.uploaded_file.name + '.asc'

        # Delete the existing .asc file to prevent duplicate
        # signature files per version on S3 and to always have
        # accurate checksums and signatures based on one file
        # only as overwriting the file is disabled
        if instance.sig_file.storage.exists(instance.sig_file.name):
            instance.sig_file.storage.delete(instance.sig_file.name)

        if instance.signature:
            instance.sig_file.save(sig_file_name, ContentFile((instance.signature).encode('utf')), save=False)
            VersionCode.objects.filter(pk=instanceid).update(sig_file=sig_file_name)

            logger.info(f"[INFO] (Task) Writing signature file ({sig_file_name}) to s3: {settings.AWS_STORAGE_BUCKET_NAME}{instance.s3_key}")
            s3_res.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                ContentType=content_type,
                StorageClass='REDUCED_REDUNDANCY',
                Key=instance.s3_key.strip('/') + '.asc',
                Body=instance.signature)
        else:
            logger.error(f"[ERROR] (Task) Writing signature file ({sig_file_name}) to s3 has failed! (No signature was found to create the asc file)")

    update_config_json()


def update_binaries():

    from tools.updater import Updater

    upd = Updater()
    upd.update_apks()
