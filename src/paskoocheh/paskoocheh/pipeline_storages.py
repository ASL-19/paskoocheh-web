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


"""Pipeline storages."""

import json
from collections import OrderedDict
from urllib.parse import unquote, urlsplit, urlunsplit

from django.core.files.base import ContentFile
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.contrib.staticfiles.utils import matches_patterns
from django.conf import settings
from pipeline.storage import GZIPMixin, PipelineMixin
from storages.backends.s3boto3 import S3Boto3Storage


class S3PipelineManifestStorage(GZIPMixin, PipelineMixin, HashedFilesMixin, S3Boto3Storage):
    """Custom storage combining GZIP, Pipeline, ManifestFiles and S3"""

    manifest_version = '1.0'  # the manifest format standard
    manifest_name = 'staticfiles.json'
    manifest_strict = False
    location = settings.STATICFILES_LOCATION
    file_overwrite = False  # from S3Boto3Storage to tell S3 not to overwrite files with the same name

    def __init__(self, *args, **kwargs):
        """
        Override django.contrib.staticfiles.storage.HashedFilesMixin.patterns
        to include handling for manifest.webmanifest and browserconfig.xml
        image references.
        """
        self.patterns = tuple(self.patterns) + (
            ("*webfrontend/manifest.webmanifest", (
                (r'("src": "(.*)")', '"src": "%s"'),
            )),
            ("*webfrontend/browserconfig.xml", (
                (r'(src="(.*)")', 'src="%s"'),
            )),
        )
        super(S3PipelineManifestStorage, self).__init__(*args, **kwargs)
        self.hashed_files = self.load_manifest()

    def read_manifest(self):
        try:
            with self.open(self.manifest_name) as manifest:
                return manifest.read().decode()
        except IOError:
            return None

    def load_manifest(self):
        content = self.read_manifest()
        if content is None:
            return OrderedDict()
        try:
            stored = json.loads(content, object_pairs_hook=OrderedDict)
        except json.JSONDecodeError:
            pass
        else:
            version = stored.get('version')
            if version == '1.0':
                return stored.get('paths', OrderedDict())
        raise ValueError("Couldn't load manifest '%s' (version %s)" %
                         (self.manifest_name, self.manifest_version))

    def post_process(self, *args, **kwargs):
        self.hashed_files = OrderedDict()
        yield from super().post_process(*args, **kwargs)
        self.save_manifest()

    def save_manifest(self):
        payload = {'paths': self.hashed_files, 'version': self.manifest_version}
        if self.exists(self.manifest_name):
            self.delete(self.manifest_name)
        contents = json.dumps(payload).encode()
        self._save(self.manifest_name, ContentFile(contents))

    def stored_name(self, name):
        parsed_name = urlsplit(unquote(name))
        clean_name = parsed_name.path.strip()
        hash_key = self.hash_key(clean_name)
        cache_name = self.hashed_files.get(hash_key)
        if cache_name is None:
            if self.manifest_strict:
                raise ValueError("Missing staticfiles manifest entry for '%s'" % clean_name)
            cache_name = self.clean_name(self.hashed_name(name))
        unparsed_name = list(parsed_name)
        unparsed_name[2] = cache_name
        # Special casing for a @font-face hack, like url(myfont.eot?#iefix")
        # http://www.fontspring.com/blog/the-new-bulletproof-font-face-syntax
        if '?#' in name and not unparsed_name[3]:
            unparsed_name[2] += '?'
        return urlunsplit(unparsed_name)

    def url(self, name, force=False):
        gzip_patterns = ("*.css", "*.html", "*.js")
        url = super(GZIPMixin, self).url(name, force)
        if matches_patterns(name, gzip_patterns):
            return "{0}.gz".format(url)
        return url
