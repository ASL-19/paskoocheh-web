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

from django.core.urlresolvers import clear_url_caches
from django.utils.module_loading import import_module
from django.conf import settings
from django.apps import apps
from importlib import reload
import logging


def parse_email(body):
    """
        Parsing data received from s3 to extract usable info
    """

    ccStringLn = None
    for line in body.splitlines():
        if line.startswith('Cc: '):
            ccStringLn = line

    return ccStringLn


def make_model(email):
    reload(import_module(settings.ROOT_URLCONF))
    clear_url_caches()
    model = None
    logger = logging.getLogger('django')
    logger.setLevel(logging.INFO)
    app_models = apps.get_app_config('s3_email').get_models()
    for _model in app_models:
        if _model._meta.model_name == email.lower():
            model = _model
    if model is None:
        logger.info('model ' + email + ' not found')
    return model
