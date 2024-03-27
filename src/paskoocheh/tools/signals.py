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


from paskoocheh.helpers import disable_for_loaddata
from paskoocheh.s3 import delete_s3_dir
from django.conf import settings
from paskoocheh.tasks import enable_latest_cloudfront_state_invalidate_flag


@disable_for_loaddata
def tools_changed(sender, instance, **kwargs):

    if settings.BUILD_ENV != 'local':
        from tools.tasks import update_json_config

        update_json_config()
        enable_latest_cloudfront_state_invalidate_flag()


@disable_for_loaddata
def version_code_changed(sender, instance, **kwargs):
    """
        Save new version code of model and upload version code specific binary to S3
    """

    if settings.BUILD_ENV != 'local':

        from tools.tasks import upload_file_to_s3

        upload_file_to_s3(instance.id)
        enable_latest_cloudfront_state_invalidate_flag()


@disable_for_loaddata
def version_code_deleted(sender, instance, **kwargs):
    """
        Remove deleted version code specific binary from S3
    """

    if settings.BUILD_ENV != 'local':

        appname = instance.version.tool.get_app_name()
        path = settings.VERSION_CODE_S3_PREFIX_TEMPLATE.format(
            appname=appname,
            version_code=instance.version_code)

        delete_s3_dir(settings.AWS_STORAGE_BUCKET_NAME, path)
        enable_latest_cloudfront_state_invalidate_flag()


@disable_for_loaddata
def faqs_changed(sender, instance, **kwargs):
    # Short-circuit if only click_count changed (this happens when a FAQ list
    # item is expanded)
    if (settings.BUILD_ENV == 'local' and
            'update_fields' in kwargs and
            type(kwargs['update_fields']) == frozenset and
            'click_count' in kwargs['update_fields']):
        return

    from tools.tasks import update_faq

    update_faq(instance.id)
    enable_latest_cloudfront_state_invalidate_flag()


@disable_for_loaddata
def guides_changed(sender, instance, **kwargs):

    if settings.BUILD_ENV != 'local':

        from tools.tasks import update_guide

        update_guide(instance.id)
        enable_latest_cloudfront_state_invalidate_flag()
