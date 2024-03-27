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

from django.db import models
from django.utils.translation import gettext_lazy as _


class CloudFrontState(models.Model):
    should_invalidate_during_next_cron_tick = models.BooleanField(
        default=False
    )


class DatesMixin(models.Model):

    created = models.DateTimeField(
        _('Date created'),
        auto_now_add=True,
        null=True)

    updated = models.DateTimeField(
        _('Date updated'),
        auto_now=True,
        null=True)

    class Meta:
        abstract = True
