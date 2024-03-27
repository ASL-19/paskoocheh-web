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
        },
        'django': {
            'handlers': ['application_stdout'],
            'level': LOG_LEVEL
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
        'statsweb': {
            'handlers': ['application_stdout'],
            'level': LOG_LEVEL
        },
        'tools': {
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

TELEGRAPH_TOKEN = os.environ['TELEGRAPH_TOKEN']

ALLOWED_HOSTS = ['*']

if DEBUG:
    INSTALLED_APPS += [ # noqa
        'storages',
    ]

# Database
DB_USER = os.environ['DATABASE_USER']
DB_PASSWORD = os.environ['DATABASE_PASSWORD']
DB_HOST = os.environ['DATABASE_HOST']
DB_NAME = os.environ['DATABASE_NAME']
STATS_DB_USER = os.environ['STATS_DATABASE_USER']
STATS_DB_PASSWORD = os.environ['STATS_DATABASE_PASSWORD']
STATS_DB_HOST = os.environ['STATS_DATABASE_HOST']
STATS_DB_NAME = os.environ['STATS_DATABASE_NAME']

# AWS Creds
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_CUSTOM_DOMAIN = f's3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}'

REDIS_PASS = os.environ['REDIS_PASSWORD']
REDIS_HOST = os.environ['REDIS_ADDRESS']

AWS_CLOUDFRONT_DISTRIBUTION_ID = os.environ.get('AWS_CLOUDFRONT_DISTRIBUTION_ID', '')
CF_CACHE_ENABLED = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ['REDIS_ADDRESS'],
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PASSWORD': os.environ['REDIS_PASSWORD'],
        },
        'KEY_PREFIX': PLATFORM,  # noqa
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

# Media Files
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'
MEDIA_ROOT = MEDIAFILES_LOCATION
DEFAULT_FILE_STORAGE = 'paskoocheh.media_storage.MediaStorage'

INTERNAL_IPS = ('127.0.0.1',)


# S3 Configuartion

S3_REGION = os.environ.get('S3_REGION')
# S3_CONFIG_PB = os.environ.get('S3_CONFIG_PB')
S3_APPS_CONFIG_JSON = os.environ.get('S3_APPS_CONFIG_JSON')
S3_FAQ_CONFIG_JSON = os.environ.get('S3_FAQ_CONFIG_JSON')
S3_GNT_CONFIG_JSON = os.environ.get('S3_GNT_CONFIG_JSON')
S3_REVIEWS_CONFIG_JSON = os.environ.get('S3_REVIEWS_CONFIG_JSON')
S3_DOWNLOAD_RATING_CONFIG_JSON = os.environ.get('S3_DOWNLOAD_RATING_CONFIG_JSON')
S3_VERSION = os.environ.get('S3_VERSION')
S3_TEXTS_CONFIG_JSON = os.environ.get('S3_TEXTS_CONFIG_JSON')
S3_BLOG_POSTS_JSON = os.environ.get('S3_BLOG_POSTS_JSON')

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'paskoocheh.media_storage.StaticStorage'
STATICFILES_LOCATION = 'static'
