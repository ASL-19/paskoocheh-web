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
from pyskoocheh.tmsg import ObjectCreationFailed


class Translation(object):

    def __init__(self, language, language_file):

        self.language = language

        self.texts = {}
        try:
            with open(language_file) as lang_file:
                self.texts = json.load(lang_file)
        except IOError:
            raise ObjectCreationFailed

    def text(self, name):
        """
            Returns the translation for text

            Args:
            name: name of the text

            Returns:
            Text in the language set in the object
        """

        return self.texts[name][self.language]
