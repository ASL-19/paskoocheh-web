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


"""Pipeline storage finders."""

from django.contrib.staticfiles.finders import BaseStorageFinder
from django.contrib.staticfiles.storage import staticfiles_storage


class DevelopmentPipelineFinder(BaseStorageFinder):
    """Custom storage finder used to work around Pipeline bug/limitation.

    https://github.com/jazzband/django-pipeline/issues/487#issuecomment-230700897
    """

    storage = staticfiles_storage
