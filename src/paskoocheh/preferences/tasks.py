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


from __future__ import absolute_import, unicode_literals
from preferences.configfile import update_text_json
import json
from preferences.models import AndroidDeviceProfile
from tools.libs.gpapi import config


def update_json_texts():
    update_text_json()


def update_android_device_profiles():
    devices = config.getDevicesReadableNames()

    for i, device in enumerate(devices, start=1):
        print(f"######### [{i}] #########")
        readableName = device['readableName']
        codename = device['codename']
        items = config.getItems(codename)

        props = {}
        for (key, value) in items:
            props[key] = value

        propsJSON = json.dumps(props, indent=2, sort_keys=True)

        # Update or create the device profile into the database
        profile = None
        created = None
        try:
            profile, created = AndroidDeviceProfile.objects.update_or_create(
                name=readableName,
                codename=codename,
                properties=propsJSON
            )
        except Exception as exc:
            print(f"ERROR: Creating a device profile object has failed due to:\n({exc})")

        if created:
            print(f"Added {codename} ({readableName}) successfully!")
        else:
            print(f"{codename} ({readableName}) already exists.")

    print(f"Number of devices supported by the Updater: {str(len(devices))}")
    print(f"Number of devices in the database: {str(len(AndroidDeviceProfile.objects.all()))}")
