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

from django.db import models
from django.conf import settings

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks


class HomePage(Page):
    """
    A homepage for each language
    """

    parent_page_types = [Page, ]

    max_count_per_parent = len(settings.LANGUAGES)

    class Meta:
        verbose_name = 'Home Page'
        verbose_name_plural = 'Home Pages'


class CaptionedImage(AbstractImage):
    """
    A custom Wagtail Image model to add caption and credit to Images
    """

    caption = models.CharField(
        max_length=255,
        blank=True)

    credit = models.CharField(
        max_length=255,
        blank=True)

    admin_form_fields = Image.admin_form_fields + (
        'caption',
        'credit',
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CaptionedImage,
        on_delete=models.CASCADE,
        related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


class StaticPage(Page):
    """
    Static Pages to be defined for the site
    """

    published = models.DateField(
        'Post Date')

    body = StreamField(
        [
            ('text', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
            ('link', blocks.URLBlock()),
            ('email', blocks.EmailBlock()),
            ('collapsible', blocks.StructBlock([
                ('slug', blocks.CharBlock(label='Slug')),
                ('heading', blocks.CharBlock(label='Heading', classname='full title')),
                ('text', blocks.RichTextBlock(label='Text')),
            ], icon='collapse-up')),
        ], use_json_field=True)

    image = models.ForeignKey(
        CaptionedImage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+')

    parent_page_types = [Page, HomePage, ]

    content_panels = Page.content_panels + [
        FieldPanel('published'),
        FieldPanel('body'),
        FieldPanel('image'),
    ]
