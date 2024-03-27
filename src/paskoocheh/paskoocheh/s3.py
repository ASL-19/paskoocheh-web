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
import json
import gzip
import io
from django.conf import settings
from pyskoocheh import crypto

from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def write_content_to_s3(content, key):
    """
        Write the content to S3 key

        Args:
        config_data: A dictionary containing all the data to be written
        key: The target key on S3
    """

    s3_res = boto3.resource(
        's3',
        region_name=settings.S3_REGION,
        config=boto3.session.Config(signature_version='s3v4'),
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    s3_res.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
        StorageClass='REDUCED_REDUNDANCY',
        Key=key,
        Body=content)


def write_config_to_s3(config_data, key, gzipped=False):
    """
        Writes the JSON config file to S3

        Args:
        config_data: A dictionary containing all the data to be written
    """
    if settings.IS_DEVELOPMENT:
        return

    s3_res = boto3.resource(
        's3',
        region_name=settings.S3_REGION,
        config=boto3.session.Config(signature_version='s3v4'),
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    signer = crypto.SignatureManager(settings.PGP_PRIVATE_KEY, settings.PGP_KEY_PASSWORD)
    buffer = json.dumps(config_data)
    if gzipped:
        buffer = io.StringIO()
        writer = gzip.GzipFile(None, 'wb', 9, buffer)
        writer.write(json.dumps(config_data))
        writer.close()
        buffer.seek(0)
        key += '.gz'

    signature = signer.sign_string(buffer)

    s3_res.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
        StorageClass='REDUCED_REDUNDANCY',
        Key=key,
        Body=buffer)
    s3_res.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
        StorageClass='REDUCED_REDUNDANCY',
        Key=key + '.asc',
        Body=signature)

    if gzipped:
        buffer.close()


def iterate_s3_objects(s3client, bucket, prefix):
    """ Iterate through an S3 bucket directory

    Args:
        s3client (boto3 S3 client): The client of S3
        bucket (str): The S3 bucket name
        prefix (str): The prefix of the directory to be looked up

    Returns:
        [list]: A list of object keys
    """

    paginator = s3client.get_paginator('list_objects_v2')
    result = paginator.paginate(Bucket=bucket, Prefix=prefix)
    bucket_object_list = list()
    for page in result:
        if 'Contents' in page:
            for key in page['Contents']:
                keyString = key['Key']
                bucket_object_list.append(keyString)

    return bucket_object_list


def copy_to_s3(s3client, bucket, src_key, dest_key, check_size=False):  # noqa: C901
    """ Copy an S3 object within the same bucket

    Args:
        s3client (boto3 S3 client): The client of S3
        bucket (str): The S3 bucket name
        src_key (str): The key of the source object
        dest_key (str): The key of the destination object
        check_size (bool, optional):
            Whether or not to compare the sizes of the source
            and destination before overwriting the dest object.
            Defaults to False.
    """

    if not check_size:
        try:
            copy_response = s3client.copy_object(
                Bucket=bucket,
                CopySource=f'{bucket}/{src_key}',
                Key=dest_key)

            if copy_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                logger.info('\tDONE!')
        except ClientError as e:
            logger.error(f'S3 copying of "{src_key}" failed with error: {e}')

    else:  # if both files have the same size in bytes, we don't overwrite the dest object
        try:
            src_response = s3client.head_object(
                Bucket=bucket,
                Key=src_key)

        except ClientError as e:
            logger.error(f'S3 header reading of "{src_key}" failed with error: {e}')
            return

        try:
            dest_response = s3client.head_object(
                Bucket=bucket,
                Key=dest_key)

            src_size = src_response['ResponseMetadata']['HTTPHeaders']['content-length']
            dest_size = dest_response['ResponseMetadata']['HTTPHeaders']['content-length']

            if src_size == dest_size:
                msg = f'"{dest_key}" already exists with the same content length! ({src_size})'
                logger.info(msg)

        except ClientError as e:
            if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
                logger.info(f'Copying "{src_key}" into "{dest_key}"...')
                copy_response = s3client.copy_object(
                    Bucket=bucket,
                    CopySource=f'{bucket}/{src_key}',
                    Key=dest_key)

                if copy_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    logger.info('\tDONE!')
            else:
                logger.error(f'S3 header reading of "{dest_key}" failed with error: {e}')


def get_s3_keys_size(keys_list, bucket):
    """
    Returns total size of keys in keys_list
    """
    s3 = boto3.resource('s3')
    total_size = 0
    for key in keys_list:
        try:
            total_size += s3.ObjectSummary(bucket, f'{settings.MEDIA_PREFIX}{key}').size
        except Exception as e:
            logger.error(f'Could not get size of {key}: {e}')
    return total_size


def get_s3_dir_size(bucket, path):
    """
    Returns total size of an S3 directory
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    return sum(obj.size for obj in bucket.objects.filter(Prefix=path))


def delete_s3_dir(bucket, path):
    """
    Deletes S3 directory
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    bucket.objects.filter(Prefix=path).delete()
