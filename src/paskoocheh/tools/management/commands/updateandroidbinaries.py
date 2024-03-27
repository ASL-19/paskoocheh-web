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


from django.core.management.base import BaseCommand
from tools.updater import Updater


class Command(BaseCommand):
    """
        Management command to download latest versions of
        android app either from google store or their
        download_url
    """

    help = 'Download the latest version of Android tools'

    def handle(self, *args, **options):
        """
            Main entry point for the command
        """

        upd = Updater()
        upd.update_apks()
