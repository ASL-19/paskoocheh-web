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

import os
import sys

BUILD_ENV = 'development'
DEBUG = True
LOG_LEVEL = 'INFO'
PIPELINE_ENABLED = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s %(levelname)s %(name)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'django': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
        'application_stdout': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.utils.autoreload': {
            'handlers': ['null'],
            'level': 'INFO'
        },
        'django': {
            'handlers': ['django'],
            'level': LOG_LEVEL
        },
        'django.server': {
            'handlers': ['null'],
        },
        'conffile': {
            'handlers': ['application_stdout'],
            'level': LOG_LEVEL
        },
        # app name and not the project name
        'authentication': {
            'handlers': ['application_stdout'],
            'level': LOG_LEVEL
        },
        'paskoocheh': {
            'handlers': ['application_stdout'],
            'level': LOG_LEVEL
        },
        'tools': {
            'handlers': ['application_stdout'],
            'level': LOG_LEVEL
        },
        'stats': {
            'handlers': ['application_stdout'],
            'level': LOG_LEVEL
        },
        'statsweb': {
            'handlers': ['application_stdout'],
            'level': LOG_LEVEL
        },
        'webfrontend': {
            'handlers': ['application_stdout'],
            'level': LOG_LEVEL
        },
        'updater': {
            'handlers': ['application_stdout'],
            'level': LOG_LEVEL
        },
    }
}

from paskoocheh.settings.base import * # noqa


CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

ALLOWED_HOSTS = ['*']

# Database
DB_USER = os.environ['DATABASE_USER']
DB_PASSWORD = os.environ['DATABASE_PASSWORD']
DB_HOST = os.environ['DATABASE_HOST']
STATS_DB_USER = os.environ['STATS_DATABASE_USER']
STATS_DB_PASSWORD = os.environ['STATS_DATABASE_PASSWORD']
STATS_DB_HOST = os.environ['STATS_DATABASE_HOST']
STATS_DB_NAME = os.environ['STATS_DATABASE_NAME']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'paskoocheh',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '',
    },
}

if 'test' not in sys.argv:
    DATABASES['api_engine'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': STATS_DB_NAME,
        'USER': STATS_DB_USER,
        'PASSWORD': STATS_DB_PASSWORD,
        'HOST': STATS_DB_HOST,
        'PORT': '5432',
    }

# if 'test' not in sys.argv:
#     DATABASES['api_engine'] = {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'stats_dev',
#         'USER': STATS_DB_USER,
#         'PASSWORD': STATS_DB_PASSWORD,
#         'HOST': STATS_DB_HOST,
#         'PORT': '3306',
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
#         }
#     }

# Media Files
MEDIA_ROOT = os.path.join(BASE_DIR, 'MEDIA') # noqa
MEDIA_URL = '/media/'

INTERNAL_IPS = ('127.0.0.1',)

# AWS Creds
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# S3 Configuartion

S3_REGION = os.environ.get('S3_REGION')
S3_APPS_CONFIG_JSON = os.environ.get('S3_APPS_CONFIG_JSON')
S3_FAQ_CONFIG_JSON = os.environ.get('S3_FAQ_CONFIG_JSON')
S3_GNT_CONFIG_JSON = os.environ.get('S3_GNT_CONFIG_JSON')
S3_REVIEWS_CONFIG_JSON = os.environ.get('S3_REVIEWS_CONFIG_JSON')
S3_DOWNLOAD_RATING_CONFIG_JSON = os.environ.get('S3_DOWNLOAD_RATING_CONFIG_JSON')
S3_VERSION = os.environ.get('S3_VERSION')
S3_TEXTS_CONFIG_JSON = os.environ.get('S3_TEXTS_CONFIG_JSON')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
