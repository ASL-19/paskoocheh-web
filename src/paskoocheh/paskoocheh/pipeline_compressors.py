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


"""Pipeline compressors."""

import os
from distutils.spawn import find_executable
from pipeline.compressors import SubProcessCompressor
from pipeline.conf import settings as pipeline_settings
from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured


def get_binary_path(relative_path):
    u"""Construct absolute path to compressor binary, check if it exists.

    Args:
        relative_path (string): Path from BASE_DIR (no leading slash)

    Returns:
        path

    Raises:
        ImproperlyConfigured: The binary couldn’t be found.
    """
    binary_location = os.path.join(
        django_settings.BASE_DIR,
        relative_path
    )

    executable_path = find_executable(binary_location)

    if not executable_path:
        raise ImproperlyConfigured(
            relative_path + ' missing. You probably need  to run `npm install`'
            'from the server directory.'
        )

    return binary_location


class UglifyJSCompressor(SubProcessCompressor):
    u"""Custom UglifyJS compressor for Django Pipeline.

    Raises ImproperlyConfigured exception if uglifyjs binary isn’t present in
    node_modules.
    """

    uglifyjs_binary_path = get_binary_path(
        django_settings.PIPELINE['UGLIFYJS_BINARY']
    )

    def compress_js(self, js):
        """Construct and run uglifyjs command."""
        command = (
            self.uglifyjs_binary_path,
            pipeline_settings.get('UGLIFYJS_ARGUMENTS', ''),
        )
        return self.execute_command(command, js)


class CleanCSSCompressor(SubProcessCompressor):
    u"""Custom CleanCSS compressor for Django Pipeline.

    Raises ImproperlyConfigured exception if uglifyjs binary isn’t present in
    node_modules.
    """

    cleancss_binary_path = get_binary_path(
        django_settings.PIPELINE['CLEANCSS_BINARY']
    )

    def compress_css(self, css):
        """Construct and run cleancss command."""
        command = (
            self.cleancss_binary_path,
            pipeline_settings.get('CLEANCSS_ARGUMENTS', ''),
        )
        return self.execute_command(command, css)
