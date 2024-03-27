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


import hashlib
import re
from collections import namedtuple
from functools import wraps
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.db import models
from django.db.utils import ProgrammingError
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from markdownx.models import MarkdownxField


def dictfetchall(cursor):
    """
        Return all rows from a cursor as a namedtuple

        Args,
        cursor: Connection cursor returned by execute function

        Returns:
        A namedtuple of the results

    """
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row)._asdict() for row in cursor.fetchall()]


def namedtuplefetchall(cursor):
    """
        Return all rows from a cursor as a namedtuple

        Args,
        cursor: Connection cursor returned by execute function

        Returns:
        A namedtuple of the results

    """
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def get_client_ip(request):
    x_forwarded_for = request.headers.get('x-forwarded-for')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def disable_for_loaddata(signal_handler):
    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs.get('raw'):
            # print "Skipping signal for %s %s" % (args, kwargs)
            return
        signal_handler(*args, **kwargs)
    return wrapper


def get_hashed_filename(file):
    hasher = hashlib.md5()
    file_data = file.read()
    hasher.update(file_data)
    # First 12 characters of MD5 hash (same as Django HashedFilesMixin)
    file_hash = hasher.hexdigest()[:12]

    filename_re_match = re.match(
        r'(.+)\.([^.]+)',
        file.name
    )

    if not filename_re_match:
        raise ValueError(u'Uploaded file has invalid name')

    filename_re_groups = filename_re_match.groups()

    if len(filename_re_groups) != 2:
        raise ValueError(u'Uploaded file has invalid name')

    filename_with_hash = '{pre_extension}.{hash}.{extension}'.format(
        pre_extension=filename_re_groups[0],
        hash=file_hash,
        extension=filename_re_groups[1],
    )

    return filename_with_hash


strict_slug_regex = re.compile(r'^[a-z][a-z-]*[a-z]$')


def validate_slug_strict(value):
    if not strict_slug_regex.match(value):
        raise ValidationError(
            u'Slugs can only contain lower-case a-z and “-” (hyphen), and must not begin or end with “-”'
        )


strict_platform_slug_regex = re.compile(r'^[a-z\d][a-z\d-]*[a-z\d]$')


def validate_platform_slug_strict(value):
    if not strict_platform_slug_regex.match(value):
        raise ValidationError(
            u'Platform slugs can only contain lower-case a-z, digits, and “-” (hyphen), and must not begin or end with “-”'
        )


class SearchableQuerySet(models.QuerySet):
    """
        A class to provide a QuerySet that helps with searching

        It provides a text_search filter to search records based on trigram similarity
    """

    def text_search(self, keyword, min_sim=0.1, related_list=[], fields_list=[]):
        """
            A method to search records based on trigram similarity.

            By default the method searches in title, content and tag columns

            Args:
            keyword: the keyword to search for (string)
            min_sim: minimum simliarity value to select records (float)
                default to 0.1
            related_list: list of related field to search beside title, content and tag (list of strings)
        """

        # Create a similarity tuple to extract similar records
        sim_tuple = (
            TrigramSimilarity('title', keyword),
            TrigramSimilarity('content', keyword),
            TrigramSimilarity('tag', keyword))

        for fld in fields_list:
            sim_tuple += (TrigramSimilarity(fld, keyword),)

        for rel in related_list:
            sim_tuple += (
                TrigramSimilarity(rel + '__title', keyword),
                TrigramSimilarity(rel + '__content', keyword),
                TrigramSimilarity(rel + '__tag', keyword))

        return self.annotate(similarity=Greatest(*sim_tuple)) \
            .filter(similarity__gt=min_sim) \
            .order_by('-similarity')

    def tag_search(self, keyword, min_sim=0.1, tag_fields=[]):
        """
            A method to search records based on trigram similarity.

            By default the method searches in title, content and tag columns

            Args:
            keyword: the keyword to search for (string)
            min_sim: minimum simliarity value to select records (float)
                default to 0.1
            related_list: list of related field to search beside title, content and tag (list of strings)
        """

        sim_tuple = (0,)

        # Create a similarity tuple to extract similar records
        for fld in tag_fields:
            sim_tuple += (TrigramSimilarity(fld, keyword),)

        return self.annotate(similarity=Greatest(*sim_tuple)) \
            .filter(similarity__gt=min_sim) \
            .order_by('-similarity')


class SearchableModel(models.Model):
    """
        An abstract class to present classes that needs to be searchable

        The class has three default properties that are needed for a
        model to be searchable. It also uses the SearchableQuerySet
        as its objects manager.
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Time'))
    title = models.CharField(
        max_length=256,
        verbose_name=_('Title'))
    content = MarkdownxField(
        null=True,
        blank=False,
        verbose_name=_('Content'))
    tag = models.TextField(
        max_length=8192,
        null=True,
        blank=True,
        verbose_name=_('Tags'),
        help_text=_('Note: This field is currently only used for search relevance. It isn’t displayed on the site.'))

    objects = SearchableQuerySet.as_manager()

    @property
    def objtype(self):
        """
            In order to identify different search outputs, objtype
            has to be defined in each inherited classes

            Returns:
            A string containing the object type for the search
        """

        pass

    class Meta:

        abstract = True


class SingletonModel(models.Model):

    def save(self, *args, **kwargs):
        self.pk = 1
        self.id = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        if cache.get(cls.__class__.__name__) is None:
            try:
                obj, created = cls.objects.get_or_create(pk=1)
            except ProgrammingError:
                return None

            if created:
                obj.set_cache()
        return cache.get(cls.__class__.__name__)

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    class Meta:
        abstract = True


class ReadOnlyAdmin(admin.ModelAdmin):
    """
        Disables all editing capabilities.
    """

    # change_form_template = "admin/paskoocheh/view.html"

    def __init__(self, *args, **kwargs):
        super(ReadOnlyAdmin, self).__init__(*args, **kwargs)
        self.readonly_fields = [f.name for f in self.model._meta.get_fields()]

    def get_actions(self, request):
        actions = super(ReadOnlyAdmin, self).get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def save_model(self, request, obj, form, change):
    #     pass

    def delete_model(self, request, obj):
        pass

    def save_related(self, request, form, formsets, change):
        pass
