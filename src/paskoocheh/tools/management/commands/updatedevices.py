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

import json
import configparser

from django.conf import settings
from django.core.management.base import BaseCommand
from preferences.models import AndroidDeviceProfile


class Command(BaseCommand):
    """
        Management command to update the list of devices and their properties
    """

    help = 'Add new devices to receive Android updates'

    def handle(self, *args, **options):
        """
            Main entry point for the command
        """

        devices = AndroidDeviceProfile.objects.filter(status='ready')
        count = devices.count()
        self.stdout.write(f'Adding properties for {count} new Android devices.')

        # Add device to device.properties config
        filepath = settings.DEVICE_PROPERTIES_PATH

        extra_properties = [
            'TouchScreen',
            'Keyboard',
            'Navigation',
            'ScreenLayout',
            'HasHardKeyboard',
            'HasFiveWayNavigation',
            'GL.Version',
            'Screen.Density',
            'Screen.Width',
            'Screen.Height',
            'Platforms',
            'SharedLibraries',
            'Features',
            'Locales',
            'GSF.version',
            'Vending.version',
            'Vending.versionString',
            'CellOperator',
            'SimOperator',
            'TimeZone',
            'GL.Extensions',
            'Roaming',
            'Client',
        ]

        failed = 0
        for device in devices:
            try:
                codename = device.codename
                name = device.name
                device_properties = json.loads(device.properties)

                config = configparser.ConfigParser()
                config.add_section(codename)
                config.optionxform = str

                config.set(codename, 'UserReadableName', name)
                for key, value in device_properties.items():
                    capitalized_key = key.capitalize().split('.')
                    for i in range(1, len(capitalized_key)):
                        capitalized_key[i] = capitalized_key[i].upper()
                    config.set(codename, ('.').join(capitalized_key), str(value))
                for key in extra_properties:
                    config.set(codename, key, '')

                with open(filepath, 'a') as configfile:
                    config.write(configfile)

                device.status = 'added'
                device.save()

            except Exception as e:
                failed += 1
                self.stdout.write(self.style.ERROR(f'Could not add device properties for {name} ({e})'))

        self.stdout.write('Adding properties completed.')

        if failed:
            self.stdout.write(self.style.ERROR(f'{failed} devices failed'))
