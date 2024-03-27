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

from django.core.management.base import BaseCommand
from django.core.exceptions import MultipleObjectsReturned

import json

from wagtail.models import Locale
from blog.models import Post, Category
from blog_wagtail.models import BlogIndexPage, PostPage, Topic
from static_page.models import CaptionedImage


def create_image(file, cmd):
    model = CaptionedImage
    model_name = model.__name__
    created = None

    try:
        obj, created = model.objects.get_or_create(
            title=file.name,
            defaults={'file': file})
    except MultipleObjectsReturned:
        cmd.stdout.write(
            cmd.style.WARNING(
                f'Multiple {model_name}s with filename "{file.name}" were found! '
                'Will select the first object...'))
        obj = model.objects.filter(title=file.name).first()

    if created:
        cmd.stdout.write(cmd.style.SUCCESS(f'A new {model_name} has been uploaded!'))

    return obj


class Command(BaseCommand):
    help = 'Migrate old posts from blog app to wagtail CMS'

    def handle(self, *args, **options): # noqa C901

        # Check all locales are added
        if Locale.objects.all().count() != 3:
            self.stdout.write(self.style.ERROR('[ERROR] Locales are missing. Make sure farsi, english and arabic are added.'))
            return

        # Check that Blog Index Page in Farsi exists
        try:
            BlogIndexPage.objects.get(
                locale=Locale.objects.get(language_code='fa'))
        except BlogIndexPage.DoesNotExist:
            self.stdout.write(self.style.ERROR('[ERROR] Blog Index Page in Farsi does not exist. Make sure it\'s created'))
            return

        # Create topics from categories
        for category in Category.objects.all():
            try:
                if category.name:
                    Topic.objects.create(
                        locale=Locale.objects.get(language_code='en'),
                        name=category.name,
                        slug=category.slug)
                if category.name_fa:
                    Topic.objects.create(
                        locale=Locale.objects.get(language_code='fa'),
                        name=category.name_fa,
                        slug=category.slug)
                if category.name_ar:
                    Topic.objects.create(
                        locale=Locale.objects.get(language_code='ar'),
                        name=category.name_ar,
                        slug=category.slug)

                self.stdout.write(self.style.SUCCESS('Successfully converted categories into topics.'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[ERROR] Could not add category(topic) "{category.name}" due to: {e}'))

        # Create PostPages from published blog posts
        for post in Post.objects.filter(status='p'):
            if post.language == 'fa':
                try:
                    # Get post topic/category
                    topic = Topic.objects.get(
                        slug=post.category.slug,
                        locale=Locale.objects.get(language_code='fa'))

                    # Get post image
                    featured_image = create_image(post.feature_image, self)

                    # Add post as child page of BlogIndexPage
                    post_page = PostPage(
                        title=post.title,
                        published=post.published_date,
                        featured_image=featured_image,
                        summary=post.summary,
                        body=json.dumps([{'type': 'markdown', 'value': post.content}]),
                        slug=post.slug)
                    BlogIndexPage.objects.get(
                        locale=Locale.objects.get(language_code='fa')).add_child(instance=post_page)

                    # Add topic to post
                    post_page.topics.add(topic)

                    self.stdout.write(self.style.SUCCESS(f'Successfully added post {post.title}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'[ERROR] Could not create blog post "{post.title}" due to: {e}'))
