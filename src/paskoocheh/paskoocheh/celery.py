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

# OBSOLETE ######################################################

# from __future__ import (
#     absolute_import,
#     unicode_literals
# )
# import os
# from django.conf import settings
# from celery import Celery
# from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
# assert 'BUILD_ENV' in os.environ, 'BUILD_ENV not set, don\'t forget to `export BUILD_ENV`'
# BUILD_ENV = os.environ['BUILD_ENV']
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paskoocheh.settings.' + BUILD_ENV)

# settings.IS_CELERY = True

# app = Celery('paskoocheh')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):

#     from stats.tasks import (
#         update_download,
#         update_feedback,
#         update_review,
#         update_rating
#     )
#     from tools.tasks import (
#         update_binaries
#     )

#     # Call update_binaries every night
#     sender.add_periodic_task(
#         crontab(minute=0, hour='1,4,7,10,13,17,20,23'),
#         update_binaries.s(),
#         name='Update Binaries')

#     if settings.DEBUG:
#         # Override interval if environment variable set
#         env_interval = os.environ.get('CELERY_INTERVAL', None)
#         celery_interval = int(env_interval) if env_interval else 600

#         # Call update_feedback every 10 minutes
#         sender.add_periodic_task(
#             celery_interval,
#             update_feedback.s(),
#             name='Retrieve Feedback Data')

#         # Call update_download every 10 minutes
#         sender.add_periodic_task(
#             celery_interval,
#             update_download.s(),
#             name='Retrieve Download Data')

#         # Call update_rating every 10 minutes
#         sender.add_periodic_task(
#             celery_interval,
#             update_rating.s(),
#             name='Retrieve Rating Data')

#         # Call update_review every 10 minutes
#         sender.add_periodic_task(
#             celery_interval,
#             update_review.s(),
#             name='Retrieve Review Data')
#     else:
#         # Call update_feedback every 12 hours
#         sender.add_periodic_task(
#             crontab(minute=0, hour='4, 16'),
#             update_feedback.s(),
#             name='Retrieve Feedback Data')

#         # Call update_download every hour
#         sender.add_periodic_task(
#             crontab(minute=0, hour='*/1'),
#             update_download.s(),
#             name='Retrieve Download Data')

#         # Call update_rating every 10 minutes
#         sender.add_periodic_task(
#             600,
#             update_rating.s(),
#             name='Retrieve Rating Data')

#         # Call update_review every 10 minutes
#         sender.add_periodic_task(
#             600,
#             update_review.s(),
#             name='Retrieve Review Data')
