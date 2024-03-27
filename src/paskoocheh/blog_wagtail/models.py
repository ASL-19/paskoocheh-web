# -*- coding: utf-8 -*-
# ASL19 website
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

import bs4
from django import forms
from django.db import models
from django.core.management import settings

from modelcluster.fields import ParentalManyToManyField

from wagtail import blocks
from wagtail.models import Page, TranslatableMixin
from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel

from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index

from wagtailmarkdown.blocks import MarkdownBlock

from static_page.models import CaptionedImage


class BlogIndexPage(Page):
    """
    Blog index page
    """

    description = RichTextField()
    # We include related_name='+' to avoid name collisions on relationships.
    # e.g. there are two FooPage models in two different apps,
    # and they both have a FK to Image, they'll both try to create a
    # relationship called `foopage_objects` that will throw a valueError on
    # collision.
    image = models.ForeignKey(
        CaptionedImage,
        on_delete=models.PROTECT,
        related_name='+')

    subpage_types = [
        'PostPage',
    ]

    # Only allowed to be created under root
    parent_page_types = [
        Page,
    ]

    search_fields = Page.search_fields + [
        index.SearchField('description'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('description', classname='full'),
        FieldPanel('image'),
    ]

    max_count_per_parent = len(settings.LANGUAGES)


@register_snippet
class Topic(TranslatableMixin, models.Model):
    """
    Topic model definition
    """

    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)

    class Meta:
        unique_together = [
            ('slug', 'locale_id'),
            ('translation_key', 'locale')
        ]

    def __str__(self):
        return f'{self.name}'


class PostPageForm(WagtailAdminPageForm):
    """
    Project page form definition
    """

    def __init__(self, *args, **kwargs):
        super(PostPageForm, self).__init__(*args, **kwargs)

        # Limit choices of issues to those of the same locale as the ProjectPage
        self.fields['topics'].queryset = Topic.objects.filter(locale=self.instance.locale)


class PostPage(Page):
    """
    A django model to define the blog post page
    """

    published = models.DateField(
        'Post date')
    featured_image = models.ForeignKey(
        CaptionedImage,
        on_delete=models.PROTECT,
        related_name='+')
    read_time = models.FloatField(
        null=True,
        blank=True)
    synopsis = models.TextField(
        blank=True)
    summary = RichTextField(
        blank=True)
    body = StreamField(
        [
            ('markdown', MarkdownBlock(icon='code')),
            ('text', blocks.RichTextBlock()),
            ('image', ImageChooserBlock()),
            ('collapsible', blocks.StructBlock([
                ('slug', blocks.CharBlock(label='Slug')),
                ('heading', blocks.CharBlock(label='Heading', classname='full title')),
                ('text', blocks.RichTextBlock(label='Text')),
            ], icon='collapse-up')),
        ], use_json_field=True)
    topics = ParentalManyToManyField(
        Topic,
        related_name='posts',
        blank=True)

    base_form_class = PostPageForm

    def word_count(self, html):
        WORD_LENGTH = 5

        def extract_text(html):
            soup = bs4.BeautifulSoup(html, 'html.parser')
            texts = soup.findAll(text=True)
            return texts

        def is_visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif isinstance(element, bs4.element.Comment):
                return False
            elif element.string == '\n':
                return False
            return True

        def filter_visible_text(page_texts):
            return filter(is_visible, page_texts)

        def count_words_in_text(text_list, word_length):
            total_words = 0
            for current_text in text_list:
                total_words += len(current_text) / word_length
            return total_words

        texts = extract_text(html)
        filtered_text = filter_visible_text(texts)
        return count_words_in_text(filtered_text, WORD_LENGTH)

    def save(self, *args, **kwargs):
        """
        Calculate read_time if it's not provided
        from: https://github.com/assafelovic/reading_time_estimator
        """

        WPM = 200.0
        total_words = 0.0
        for block in self.body:
            if block.block.__class__.__name__ in ('CharBlock', 'RichTextBlock'):
                total_words += self.word_count(str(block.value))

        self.read_time = total_words / WPM

        super(PostPage, self).save(*args, **kwargs)

    # Only allowed to be created under root
    parent_page_types = [
        'BlogIndexPage',
    ]

    # Specifies what content types can exist as children of PostPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('published'),
        FieldPanel('featured_image'),
        FieldPanel('topics', widget=forms.CheckboxSelectMultiple),
        FieldPanel('read_time', widget=forms.TextInput(attrs={"disabled": True})),
        FieldPanel('synopsis', classname='full'),
        FieldPanel('summary'),
        FieldPanel('body'),
    ]
