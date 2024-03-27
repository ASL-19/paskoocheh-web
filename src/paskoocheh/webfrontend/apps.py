# coding: utf-8
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

u"""
Webfrontend app config.
"""

import logging
import re
from django.apps import AppConfig
# from django.conf import settings
from django.template import base

logger = logging.getLogger(__name__)


class WebfrontendConfig(AppConfig):
    name = 'webfrontend'
    verbose_name = u'Webfrontend'

    def ready(self):
        u"""
        Runs once when app is initialized.
        https://stackoverflow.com/a/16111968/7949868
        """

        # Hack to allow multi-line template tags
        # http://zachsnow.com/#!/blog/2016/multiline-template-tags-django/
        base.tag_re = re.compile(base.tag_re.pattern, re.DOTALL)

        # on server startup, this will ensure that download counts and ratings are to be populated into redis (stats cache)
        # if os.environ.get('RUN_MAIN', False):
        #     import webfrontend.caches.stats.register_signal_handlers  # noqa
        #     logger.info('Scheduling update of download counts and ratings to ensure webfrontend stats cache is populated.')

        #     from stats.tasks import (
        #         update_download,
        #         update_rating,
        #     )

        #     update_download(self)
        #     update_rating(self)
