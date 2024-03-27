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

from tools.configfile import update_config_json
from paskoocheh.s3 import iterate_s3_objects, copy_to_s3, get_s3_dir_size, get_s3_keys_size, delete_s3_dir

from tools.models import Version, Tool, Guide, Tutorial, Faq
from blog.models import Post

logger = logging.getLogger(__name__)


def keys_list(*querysets):
    """
    Converts tuples from querysets to list of keys(files)
    """
    list = []
    for queryset in querysets:
        if queryset:
            list.extend([item[0] for item in queryset if item[0]])
    return list


class Command(BaseCommand):
    """
    Updates S3_INTERNET_SHUTDOWN_DIR directory in S3 with the latest content of:
    CONFIG_PREFIX dir (except S3_APPS_CONFIG_JSON, S3_FAQ_CONFIG_JSON, and S3_GNT_CONFIG_JSON), MEDIA_PREFIX dir, and TOOLS_PREFIX dir (only internet-shutdown tools)
    and updates the S3_APPS_CONFIG_JSON file to reflect the internet-shutdown tool changes, if any.
    """

    help = '''Updates S3_INTERNET_SHUTDOWN_DIR directory in S3 with the latest content of:
    CONFIG_PREFIX dir (except S3_APPS_CONFIG_JSON, S3_FAQ_CONFIG_JSON, and S3_GNT_CONFIG_JSON), MEDIA_PREFIX dir, and TOOLS_PREFIX dir (only internet-shutdown tools)
    and updates the S3_APPS_CONFIG_JSON file to reflect the internet-shutdown tool changes, if any.'''

    def handle(self, *args, **options):     # noqa: C901

        bucket = settings.AWS_STORAGE_BUCKET_NAME
        dir = settings.S3_INTERNET_SHUTDOWN_DIR
        apps_json = settings.S3_APPS_CONFIG_JSON.rsplit('/', 1)[1]
        faqs_json = settings.S3_FAQ_CONFIG_JSON.rsplit('/', 1)[1]
        gnt_json = settings.S3_GNT_CONFIG_JSON.rsplit('/', 1)[1]

        internet_shutdown_apps = Version.objects \
            .filter(tool__tooltype__slug='internet-shutdown-ir', supported_os__name='android') \
            .select_related('tool') \
            .prefetch_related() \
            .order_by('tool__name') \
            .all()

        s3client = boto3.client('s3')

        # Copying Tools dir
        logger.info('\n###\nCopying Internet shutdown tools from Tools dir...')
        count = len(internet_shutdown_apps)

        if count > 0:
            logger.info(f'There are currently `{count}` Internet shutdown tools in the database')

            tools_keys = list()

            # We are starting with one empty subdir
            delete_s3_dir(bucket, dir + '/')
            subdir_count = 1
            subdir = f'IS{subdir_count}'

            # Update apps, faqs, gnt for subdir apps
            logger.info(f'\n###\nUpdating config json files for {subdir}')
            update_config_json(internet_shutdown_apps)
            logger.info('\tDONE!')

            config_files_size = get_s3_dir_size(bucket, settings.CONFIG_PREFIX)

            for i, app in enumerate(internet_shutdown_apps, start=1):
                appname = app.tool.get_app_name()

                logger.info(f'[{i}] {app}')

                # Get all app related media
                logger.info(f'Getting related media to {appname}...')
                posts_tool_tags_images = Post.objects.filter(
                    tool_tag__in=Tool.objects.filter(
                        versions=app)
                ).values_list('feature_image').distinct()

                posts_version_tags_images = Post.objects.filter(
                    version_tag=app
                ).values_list('feature_image').distinct()

                posts_tool_tags_videos = Post.objects.filter(
                    tool_tag__in=Tool.objects.filter(
                        versions=app)
                ).values_list('video').distinct()

                posts_version_tags_videos = Post.objects.filter(
                    version_tag=app
                ).values_list('video').distinct()

                faqs_tools_videos = Faq.objects.filter(
                    tool__in=Tool.objects.filter(
                        versions=app)
                ).values_list('video').distinct()

                faqs_version_videos = Faq.objects.filter(
                    version=app
                ).values_list('video').distinct()

                guide_version_videos = Guide.objects.filter(
                    version=app
                ).values_list('video').distinct()

                tutorial_version_videos = Tutorial.objects.filter(
                    version=app
                ).values_list('video').distinct()

                tools_images = []
                for tool in Tool.objects.filter(versions=app):
                    tools_images.extend(tool.images.all().values_list('image').distinct())

                versions_images = app.images.all().values_list('image').distinct()

                blog_keys = keys_list(
                    posts_tool_tags_images,
                    posts_version_tags_images)

                video_keys = keys_list(
                    posts_tool_tags_videos,
                    posts_version_tags_videos,
                    faqs_tools_videos,
                    faqs_version_videos,
                    guide_version_videos,
                    tutorial_version_videos)

                img_keys = keys_list(
                    tools_images,
                    versions_images)

                all_media_keys = blog_keys + video_keys + img_keys
                tool_media_size = get_s3_keys_size(all_media_keys, bucket)
                logger.info(f'Size of related media to "{appname}" = {tool_media_size}')

                tooltype_size = get_s3_dir_size(bucket, f'{settings.MEDIA_PREFIX}{settings.TOOLTYPE_PATH}')
                promo_size = get_s3_dir_size(bucket, f'{settings.MEDIA_PREFIX}{settings.PROMOIMAGE_PATH}')
                common_media_size = tooltype_size + promo_size
                common_files_size = common_media_size + config_files_size
                logger.info(f'Size of common files = {common_files_size}')

                tool_app_size = get_s3_dir_size(bucket, settings.ANDROID_TOOLS_PREFIX_TEMPLATE.format(appname=appname).split(settings.ANDROID_PREFIX))
                logger.info(f'Size of app "{appname}" = {tool_app_size}')

                tool_size = tool_app_size + tool_media_size
                logger.info(f'Total Size of tool "{appname}" = {tool_size}')

                subdir_size = get_s3_dir_size(bucket, f'{dir}/{subdir}/')
                logger.info(f'Size of subdir "{subdir}" = {subdir_size}')

                # If we will exceed maximum allowed subdir size, we need to update CONFIG_PREFIX and
                # MEDIA_PREFIX dirs in this subdir and start with a new subdir
                if subdir_size + tool_size + common_files_size > settings.IS_SPLIT_SIZE:
                    logger.info(f'Subdir "{subdir}" is full. Wrapping up...')

                    # Copy apps_json, faqs_json, gnt_json to subdir
                    for file in [apps_json, faqs_json, gnt_json]:
                        key = f'{dir}/{settings.CONFIG_PREFIX}{file}'
                        dest_key = f'{dir}/{subdir}/{settings.CONFIG_PREFIX}{file}'
                        copy_to_s3(s3client, bucket, key, dest_key, check_size=True)

                    config_prefix = settings.CONFIG_PREFIX

                    config_keys = iterate_s3_objects(s3client, bucket, config_prefix)
                    for j, key in enumerate(config_keys, start=1):
                        # Skip apps, faqs, and gnt (guides and tutorials) config files
                        if any(x in key for x in (apps_json, faqs_json, gnt_json)):
                            logger.info(f'[{j}] Skipping {key}')
                            continue

                        dest_key = f'{dir}/{subdir}/{key}'
                        copy_to_s3(s3client, bucket, key, dest_key, check_size=True)

                    media_prefix = settings.MEDIA_PREFIX

                    media_keys = iterate_s3_objects(s3client, bucket, media_prefix)
                    for j, key in enumerate(media_keys, start=1):
                        # Skip any non-relevant media files
                        if not any(x in key for x in (settings.PROMOIMAGE_PATH, settings.TOOLTYPE_PATH)):
                            logger.info(f'[{j}] Skipping {key}')
                            continue

                        dest_key = f'{dir}/{subdir}/{key}'
                        copy_to_s3(s3client, bucket, key, dest_key, check_size=True)

                    # Creating new subdir and resetting size
                    subdir_count += 1
                    subdir = f'IS{subdir_count}'
                    logger.info(f'New subdir: "{subdir}" created.')

                if blog_keys:
                    for key in blog_keys:
                        key = f'{settings.MEDIA_PREFIX}{key}'
                        dest_key = f'{dir}/{subdir}/{key}'
                        logger.info(f'Copying "{appname}" blog related media "{key}" into "{subdir}"')
                        copy_to_s3(s3client, bucket, key, dest_key, check_size=True)

                if video_keys:
                    for key in video_keys:
                        key = f'{settings.MEDIA_PREFIX}{key}'
                        dest_key = f'{dir}/{subdir}/{key}'
                        logger.info(f'Copying "{appname}" related videos "{key}" into "{subdir}"')
                        copy_to_s3(s3client, bucket, key, dest_key, check_size=True)

                if img_keys:
                    for key in img_keys:
                        key = f'{settings.MEDIA_PREFIX}{key}'
                        dest_key = f'{dir}/{subdir}/{key}'
                        logger.info(f'Copying "{appname}" related images "{key}" into "{subdir}"')
                        copy_to_s3(s3client, bucket, key, dest_key, check_size=True)

                try:
                    tools_prefix = settings.ANDROID_TOOLS_PREFIX_TEMPLATE.format(appname=appname).split(settings.ANDROID_PREFIX)

                    tools_keys.extend(iterate_s3_objects(s3client, bucket, tools_prefix))

                    for j, key in enumerate(tools_keys, start=1):
                        if key.find(f'/{settings.ANDROID_PREFIX}') < 0:
                            continue
                        logger.info(f'[{i}.{j}] Copying "{key}" into "{dir}/{subdir}/{key}"...')

                        dest_key = f'{dir}/{subdir}/{key}'
                        copy_to_s3(s3client, bucket, key, dest_key)

                    if len(tools_keys) == 0:
                        logger.warn(f'No S3 keys found for "{app}"')
                    # Clear the keys (files) list
                    tools_keys.clear()

                except ClientError as e:
                    logger.error('S3 tools copy failed with error: ' + e.message)

            logger.info(f'Subdir "{subdir}" is the last one. Wrapping up...')

            # Copy apps_json, faqs_json, gnt_json to subdir
            for file in [apps_json, faqs_json, gnt_json]:
                key = f'{dir}/{settings.CONFIG_PREFIX}{file}'
                dest_key = f'{dir}/{subdir}/{settings.CONFIG_PREFIX}{file}'
                copy_to_s3(s3client, bucket, key, dest_key, check_size=True)

            config_prefix = settings.CONFIG_PREFIX

            config_keys = iterate_s3_objects(s3client, bucket, config_prefix)
            for j, key in enumerate(config_keys, start=1):
                # Skip apps, faqs, and gnt (guides and tutorials) config files
                if any(x in key for x in (apps_json, faqs_json, gnt_json)):
                    logger.info(f'[{j}] Skipping {key}')
                    continue

                dest_key = f'{dir}/{subdir}/{key}'
                copy_to_s3(s3client, bucket, key, dest_key, check_size=True)

            media_prefix = settings.MEDIA_PREFIX

            media_keys = iterate_s3_objects(s3client, bucket, media_prefix)
            for j, key in enumerate(media_keys, start=1):
                # Skip any non-relevant media files
                if not any(x in key for x in (settings.PROMOIMAGE_PATH, settings.TOOLTYPE_PATH)):
                    logger.info(f'[{j}] Skipping {key}')
                    continue

                dest_key = f'{dir}/{subdir}/{key}'
                copy_to_s3(s3client, bucket, key, dest_key, check_size=True)

            delete_s3_dir(bucket, f'{dir}/{settings.CONFIG_PREFIX}')

        else:
            logger.warn('There are no Internet Shutdown tools in the database at this time.')
