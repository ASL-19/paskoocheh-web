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

u"""webfrontend stats cache signal handlers registration.

Note: Registers signal handlers when imported!

Updates stats caches in response to VersionDownload/VersionRating
post_batch_update signals.

The aforementioned signals are sent from stats.tasks.update_download and
stats.tasks.update_update_rating respectively
"""

import logging
from stats.models import VersionDownload, VersionRating
from stats.signals import post_batch_update
from webfrontend.caches.stats.signal_handlers import (
    update_versiondownload_cache_values,
    update_versionrating_cache_values,
)

logger = logging.getLogger(__name__)


logger.info(u'Registering signal handlers')

post_batch_update.connect(
    update_versiondownload_cache_values,
    sender=VersionDownload,
    weak=False,
)

post_batch_update.connect(
    update_versionrating_cache_values,
    sender=VersionRating,
    weak=False,
)
