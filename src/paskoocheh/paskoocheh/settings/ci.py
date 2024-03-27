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

BUILD_ENV = 'ci'
DEBUG = True
LOG_LEVEL = 'DEBUG'

from paskoocheh.settings.base import *

ALLOWED_HOSTS = ['*']

# Database
DB_USER = os.environ['DATABASE_USER']
DB_PASSWORD = os.environ['DATABASE_PASSWORD']
DB_HOST = os.environ['DATABASE_HOST']
DB_NAME = os.environ['DATABASE_NAME']
DB_PORT = os.environ['DATABASE_PORT']

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

# Media Files
MEDIA_ROOT = os.path.join(BASE_DIR, 'MEDIA')
MEDIA_URL = '/media/'
MEDIAFILES_LOCATION = MEDIA_URL

STATICFILES_LOCATION = STATIC_URL

INTERNAL_IPS = ('127.0.0.1',)
