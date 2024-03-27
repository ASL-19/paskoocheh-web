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


from django.conf import settings
from paskoocheh.s3 import write_config_to_s3
from preferences.models import Text


def update_text_json():
    """
        Updates the json static texts file
    """

    texts = Text.objects.all()
    results = []

    for text in texts:
        results.append({
            u'id': text.id,
            u'language': text.language,
            u'last_modified': text.last_modified.strftime(u'%Y-%m-%d %H:%M:%S'),
            u'about': text.about,
            u'contact_email': text.contact_email,
            u'privacy_policy': text.privacy_policy,
            u'terms_of_service': text.terms_of_service,
            u'terms_and_privacy': text.terms_and_privacy
        })

    write_config_to_s3(results, settings.S3_TEXTS_CONFIG_JSON)
