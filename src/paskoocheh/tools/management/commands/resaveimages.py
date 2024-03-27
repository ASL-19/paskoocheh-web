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
from tools.models import Image
from preferences.models import PromoImage

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Command that calls save() on all existing tools.Image instances to set
    Image.width and Image.height. Will also generate warnings for images with
    missing files.
    """
    help = (
        'Calls save() on all existing tools.Image instances to set '
        'Image.width and Image.height. Will also generate warnings for images '
        'with missing files.'
    )

    def handle(self, *args, **options):
        """
        Command method.
        """
        # Images
        all_images = Image.objects.all()

        logger.info(
            'Calling save() on {length} tools.Image instances'.format(
                length=all_images.count()
            )
        )

        for image in all_images:
            image.save()

        # PromoImages
        all_promo_images = PromoImage.objects.all()

        logger.info(
            'Calling save() on {length} preferences.PromoImage instances'.format(
                length=all_promo_images.count()
            )
        )

        for promo_image in all_promo_images:
            promo_image.save()
