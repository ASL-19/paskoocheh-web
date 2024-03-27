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
import time

import boto3

from botocore.exceptions import ClientError
from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import CloudFrontState

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    u"""
    Invalidates CloudFront if an invalidation has been requested by app
    code (e.g. a model signal).

    This command looks at the first (and only, unless something’s wrong)
    instance of models.CloudFrontState and invalidates if
    should_invalidate_during_next_cron_tick is True.

    If the --force argument is passed to the command, the invalidation
    will run even if it hasn’t been requested by the app code. This may
    be useful for running on deploy.
    """

    help = u'Invalidates CloudFront if an invalidation has been requested by app code (e.g. a model signal).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true'
        )

    def handle(self, *args, **options):

        if ((hasattr(settings, 'CF_CACHE_ENABLED') and settings.CF_CACHE_ENABLED is False) or
                not hasattr(settings, 'AWS_CLOUDFRONT_DISTRIBUTION_ID') or
                not isinstance(settings.AWS_CLOUDFRONT_DISTRIBUTION_ID, str) or
                len(settings.AWS_CLOUDFRONT_DISTRIBUTION_ID) == 0):
            self.stdout.write(u'Skipping CloudFront invalidation since AWS_CLOUDFRONT_DISTRIBUTION_ID isn’t set')

            return

        cloudfront_state = CloudFrontState.objects.first()

        if (
            options['force'] is False and
            (
                not isinstance(cloudfront_state, CloudFrontState) or
                cloudfront_state.should_invalidate_during_next_cron_tick is False
            )
        ):
            self.stdout.write(u'CloudFront didn’t need to be invalidated')

            return

        cloudfront_client = boto3.client('cloudfront')

        try:
            # ----------------------------
            # --- Request invalidation ---
            # ----------------------------
            cloudfront_client.create_invalidation(
                DistributionId=settings.AWS_CLOUDFRONT_DISTRIBUTION_ID,
                InvalidationBatch={
                    'Paths': {
                        'Quantity': 1,
                        'Items': ['/*'],
                    },
                    'CallerReference': str(time.time()),
                }
            )

            # ------------------------------------------------------------
            # --- Set should_invalidate_during_next_cron_tick to False ---
            # ------------------------------------------------------------
            if isinstance(cloudfront_state, CloudFrontState):
                cloudfront_state.should_invalidate_during_next_cron_tick = False
                cloudfront_state.save()
            else:
                new_cloudfront_state = CloudFrontState(
                    should_invalidate_during_next_cron_tick=True
                )
                new_cloudfront_state.save()

            self.stdout.write(u'Invalidated CloudFront')
        except ClientError as error:
            self.stdout.write(u'CloudFront invalidation failed with error: ' + error.message)
