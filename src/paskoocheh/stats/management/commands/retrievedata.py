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
from stats.tasks import (
    update_download,
    update_rating,
    update_review,
    update_feedback
)


class Command(BaseCommand):
    """
        Management command to retrieve the latest tools stats
        data from remote database.
    """

    help = 'Retrive the latest data from remote database'

    def handle(self, *args, **options):
        """
            Main entry point for the command
        """

        import webfrontend.caches.stats.register_signal_handlers  # noqa

        appLabel = '[Stats Tasks]'
        self.stdout.write(appLabel)
        self.stdout.flush()

        msg = 'Updating the download data...'
        self.stdout.write(msg)
        self.stdout.flush()
        update_download(self)

        msg = 'Updating the rating data...'
        self.stdout.write(msg)
        self.stdout.flush()
        update_rating(self)

        msg = 'Updating the review data...'
        self.stdout.write(msg)
        self.stdout.flush()
        update_review(self)

        msg = 'Updating the feedback data...'
        self.stdout.write(msg)
        self.stdout.flush()
        update_feedback(self)

        msg = 'Successfully updated the local database'
        self.stdout.write(msg)
        self.stdout.flush()
