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
from django.core.files.images import get_image_dimensions

logger = logging.getLogger('tools')


class ImageWithCachedDimensionsMixin(object):
    """
    Mixin for images with cached dimensions (top-level width and height
    attributes).
    """

    def save_image_dimensions(self):
        """
        Populate top-level width and height attributes. While these are also
        available in image.width and image.height, it’s preferable to store
        them so that the image files don’t need to be opened/downloaded from S3
        in order to know the dimensions during a request.
        """

        # If a new or replacement image is being uploaded, look at the size
        # tuple of image._file (InMemoryUploadedFile) to get the dimensions.
        if (
            hasattr(self.image, '_file') and
            hasattr(self.image._file, 'image') and
            hasattr(self.image._file.image, 'size') and
            self.image._file.image.size[0] > 0 and
            self.image._file.image.size[1] > 0
        ):
            self.width = self.image._file.image.size[0]
            self.height = self.image._file.image.size[1]
        # If the image isn’t being changed (e.g. a save has been manually
        # triggered, or a different field is being changed), use image.file to
        # get the dimensions.
        elif hasattr(self.image, 'file'):
            dimensions = get_image_dimensions(self.image.file)
            if dimensions[0] > 0 and dimensions[1] > 0:
                self.width = dimensions[0]
                self.height = dimensions[1]
        else:
            logger.warning(
                u'Wasn’t able to set width and height attributes of tools.Image {id}. This could happen if the associated image file doesn’t exist.'.format(
                    id=self.id
                )
            )
