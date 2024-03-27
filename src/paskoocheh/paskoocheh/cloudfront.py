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
import re

import boto3

from django.conf import settings
from django.db.models import Model

from django.db.models.signals import post_delete, post_save

logger = logging.getLogger(__name__)

cloudfront_client = boto3.client('cloudfront')

frontend_modules_regex = re.compile(r'^(?:static_page|blog_wagtail|preference|rewards|stats|tools)\..*')


def register_request_cloudfront_invalidation_signal_handlers():
    for signal in (post_delete, post_save,):
        signal.connect(request_cloudfront_invalidation_if_appropriate)


def request_cloudfront_invalidation_if_appropriate(*args, **kwargs):
    sender_module = getattr(
        kwargs.get('sender', None),
        '__module__',
        '')

    if not frontend_modules_regex.search(sender_module):
        logger.info(
            f'Not requesting CloudFront invalidation since sender "{sender_module}" isn’t a frontend module')
        return

    instance = kwargs.get('instance', None)

    if (isinstance(instance, Model) and
            getattr(instance, '_is_updating_cache_fields', False)):
        logger.info('Not requesting CloudFront invalidation since instance is updating cache fields')
        return

    request_cloudfront_invalidation()


def request_cloudfront_invalidation():
    if (not hasattr(settings, 'AWS_CLOUDFRONT_DISTRIBUTION_ID') or
            not isinstance(settings.AWS_CLOUDFRONT_DISTRIBUTION_ID, str)):
        logger.info('Requested CloudFront invalidation (disabled since AWS_CLOUDFRONT_DISTRIBUTION_ID not set)')
        return

    from .models import CloudFrontState

    cloudfront_state = CloudFrontState.objects.first()

    if isinstance(cloudfront_state, CloudFrontState):
        if cloudfront_state.should_invalidate_during_next_cron_tick is False:
            cloudfront_state.should_invalidate_during_next_cron_tick = True
            cloudfront_state.save()
    else:
        new_cloudfront_state = CloudFrontState(
            should_invalidate_during_next_cron_tick=True)
        new_cloudfront_state.save()

    logger.info('Requested CloudFront invalidation')
