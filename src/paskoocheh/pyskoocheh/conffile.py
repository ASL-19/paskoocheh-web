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

""" Conffile Module

    Holds functions for working with conffile Protocol Buffers
"""
from botocore.exceptions import ClientError
from pyskoocheh.errors import AWSError
import protobuf.schemas.python.paskoocheh_pb2 as paskoocheh
from pyskoocheh import storage


def load_config_data(bucket, key):
    """ Load configuration file

    Args:
        bucket: s3 bucket for configuration file
        key: s3 key for configuration file
    Returns:
        File contents
    Raises:
        AWSError: error getting configuration file from s3
        ValidationError: error parsing protocol buffer message
    """

    config_file = paskoocheh.ConfigFile()
    try:
        file_data = storage.get_binary_contents(bucket, key)
    except ClientError as error:
        raise AWSError("Error loading file from S3: {}".format(str(error)))
    config_file.ParseFromString(file_data)
    return config_file


def save_config_data(bucket, key, config_file):
    """ Save configuration file

    Args:
        bucket: s3 bucket to store configuration file in
        key: s3 key to store configuration file at
        conf_file: configuration file object (Protocol Buffer)
    Raises:
        AWSError: error saving configuration file to s3
    """

    file_data = config_file.SerializeToString()
    storage.put_binary_file(bucket, key, file_data)
    return
