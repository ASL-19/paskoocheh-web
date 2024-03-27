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

import logging
from django.core.management.base import BaseCommand
from tools.models import VersionCode
from django.core.files import File
import argparse

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
        Management command to store existing upload files of Version table to new version code table
    """

    help = 'backup, stores the Version - uploaded_file to new Version Code table'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=argparse.FileType('r'))
        parser.add_argument('--versioncode', type=int)

    def handle(self, *args, **options):
        """
            Main entry point for the command
        """
        uploaded_file = options['file']
        vc_id = options['versioncode']

        vc = VersionCode.objects.get(id=vc_id)

        logger.info(f'Updating version code [{vc.version_code}] of version [{vc.version.version_number}] | "{vc.version.tool.name}"...')
        try:
            vc.uploaded_file.name = uploaded_file.name
            vc.uploaded_file.save(uploaded_file.name,
                                  File(uploaded_file), save=True)
            logger.info(f'Updated version code [{vc.version_code}] of version [{vc.version.version_number}] | "{vc.version.tool.name}" successfully...')
        except Exception as e:
            logger.error(f'[ERROR] Unable to the version code [{vc.version_code}] of version [{vc.version.version_number}] | "{vc.version.tool.name}" due to: {e}')
