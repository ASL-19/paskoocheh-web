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


from __future__ import unicode_literals
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.core.management import settings
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.urls import reverse
from paskoocheh.helpers import (
    get_hashed_filename,
    SearchableModel,
    validate_slug_strict,
)
from tools.models import (
    Tool,
    Version,
)
from webfrontend.caches.responses.signal_handlers import purge_blog
from .blog_settings import LOGO_PATH, IMAGE_PATH
from .signals import blogs_changed
from preferences.models import Tag
from tools.models import (
    get_video_upload_to,
    update_video_help_text_snippet,
)


def get_category_logo_upload_to(instance, filename):
    return u'{path}/{hashed_filename}'.format(
        path=LOGO_PATH,
        hashed_filename=get_hashed_filename(instance.logo.file)
    )


class Category(models.Model):
    """
        Model to represent Blog posts' categories.
    """
    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Time'))
    name = models.CharField(
        max_length=32,
        verbose_name=_('Category Name (English)'),
        null=False,
        blank=False)
    name_ar = models.CharField(
        max_length=32,
        verbose_name=_('Category Name (Arabic)'),
        null=True,
        blank=True)
    name_fa = models.CharField(
        max_length=32,
        verbose_name=_('Category Name (Farsi)'),
        null=True,
        blank=False)
    slug = models.SlugField(
        blank=False,
        max_length=128,
        null=True,
        unique=True,
        validators=[validate_slug_strict])
    logo = models.ImageField(
        upload_to=get_category_logo_upload_to,
        null=True,
        blank=True,
        verbose_name=_('Photo'),
        help_text=_('Note: This is currently unused.'))
    description = models.TextField(
        null=True,
        blank=False,
        verbose_name=_('Description'),
        help_text=_('Not displayed on site, but used as social media description and search engine snippet suggestion for blog category pages.'))

    def __str__(self):

        return self.name

    @property
    def admin_thumbnail(self):
        """
            Return an image to be displayed in admin panel

            Returns:
            An html to image logo if exists or a text of no image otherwise.
        """

        if self.logo:
            return mark_safe("<img src='{}' height='100' />".format(self.logo.url))
        else:
            return "( No Image )"

    class Meta:

        verbose_name_plural = _('Categories')


post_save.connect(blogs_changed, sender=Category)
post_delete.connect(blogs_changed, sender=Category)
post_save.connect(purge_blog, sender=Category)
post_delete.connect(purge_blog, sender=Category)


def get_post_feature_image_upload_to(instance, filename):
    return u'{path}/{hashed_filename}'.format(
        path=IMAGE_PATH,
        hashed_filename=get_hashed_filename(instance.feature_image.file)
    )


class Post(SearchableModel):
    """
        Model to represent the blog posts

        This model is a based on SearchableModel in order to
        facilitate the trigram search.
    """
    POST_STATUS_CHOICES = (
        ('p', 'Published'),
        ('d', 'Draft'))

    published_date = models.DateTimeField(
        null=False,
        blank=False,
        default=timezone.now,
        verbose_name=_('Published Date'))
    # published_date_is_final is used to determine if the published_date field
    # should be treated as final, and therefore immutable. If a post is saved
    # as a draft, published_date is set to timezone.now so that the post can
    # be previewed by visiting it’s unadvertised URL, which contains the date.
    # If a post’s status changes from draft to published and
    # published_date_final is False, the published_date field is updated to
    # timezone.now, and published_date_final is set to True. This is necessary
    # to make sure the post’s published date is set correctly upon publication
    # (i.e. isn’t still set to the date it was originally saved a draft), and
    # that it can’t be changed in the future, which would break existing URLs.
    published_date_is_final = models.BooleanField(
        default=False)
    category = models.ForeignKey(
        'Category',
        related_name='post',
        verbose_name=_('Category'),
        null=True,
        blank=False,
        on_delete=models.CASCADE)
    summary = models.TextField(
        null=True,
        blank=False,
        verbose_name=_('Summary'),
        help_text=_('Used for post listing previews if the post has no associated featured image. Also appears in RSS feeds, social media preview, and search engine snippets.'))
    slug = models.SlugField(
        max_length=128,
        unique=True,
        validators=[validate_slug_strict])
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        help_text=_('Note: The post‘s associated user is not currently displayed on the site, but this may change in the future.'),
        related_name='review',
        null=True,
        on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=1,
        choices=POST_STATUS_CHOICES,
        default='d')
    comment_allowed = models.BooleanField(
        default=False,
        verbose_name=_('Comments Allowed'),
        help_text=_('Note: Comments aren’t currently supported, but this may change in the future.'),)
    tool_tag = models.ManyToManyField(
        Tool,
        related_name='blog_posts',
        verbose_name='Associated Tools',
        blank=True)
    version_tag = models.ManyToManyField(
        Version,
        related_name='blog_posts',
        verbose_name='Associated Versions',
        blank=True)
    homepage_feature = models.PositiveIntegerField(
        blank=True,
        null=True,
        unique=True,
        verbose_name=_('Feature Order'),
        help_text=_('If set, the post will be considered featured. Featured posts with lower feature orders will appear earlier in featured lists.'))
    feature_image = models.ImageField(
        upload_to=get_post_feature_image_upload_to,
        null=True,
        blank=True,
        verbose_name=_('Featured Image'),
        help_text=_('Feature images should have a 2.5:1 aspect ratio (e.g. 800x320). This target ratio can be changed with minor changes to the site, but it needs to be consistent across all blog posts.'))
    feature_image_caption = models.CharField(
        max_length=2048,
        null=True,
        blank=True,
        verbose_name=_('Featured Image Description'),
        help_text=_('Text describing the image (for screen readers and search engines)'))
    language = models.CharField(
        max_length=2,
        default=settings.LANGUAGE_SUPPORTED_DEFAULT,
        choices=settings.LANGUAGE_SUPPORTED_CHOICES,
        verbose_name=_('Language'))
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("Tags"),
        related_name=('posts'),
        blank=True)
    video = models.FileField(
        upload_to=get_video_upload_to,
        null=True,
        blank=True,
        verbose_name=_('Video File'),
        help_text='Once the file to be uploaded has been saved, an HTML code snippet will be provided.')

    def save(self, *args, **kwargs):
        if self.status == 'p' and not self.published_date_is_final:
            self.published_date = timezone.now()
            self.published_date_is_final = True

        if self.video:
            try:
                field = self._meta.get_field('video')
                field.help_text = update_video_help_text_snippet(self.video)
            except Exception:
                pass
        super(Post, self).save(*args, **kwargs)

    @property
    def tool_tag_list(self):
        return [x.id for x in self.tool_tag.all()]

    @property
    def version_tag_list(self):
        return [x.id for x in self.version_tag.all()]

    @property
    def image_url(self):
        if self.feature_image and hasattr(self.feature_image, 'url'):
            return self.feature_image.url

    @property
    def tag_list(self):
        return [x.slug for x in self.tags.all()]

    class Meta(object):
        """
            Database metadata class
        """

        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):

        return self.title

    def get_post_link(self):
        """
            URL link to posts

            Returns:
            A URL made based on type of the post
        """

        published_date_iso8601 = self.published_date.isoformat()[:10]

        return '/blog/posts/{published_date_iso8601}-{slug}.html'.format(
            published_date_iso8601=published_date_iso8601,
            slug=self.slug,
        )

    def get_post_link_admin_display(self):
        post_url = self.get_post_link()

        if self._state.adding:
            return '(Not yet saved)'

        return '<a href="{post_url}">{post_url}</a>'.format(
            post_url=post_url
        )
    get_post_link_admin_display.short_description = 'Post URL'
    get_post_link_admin_display.allow_tags = True

    def get_tool_tags_admin_list_display(self):
        return ", ".join(
            [str(tool) for tool in self.tool_tag.all()]
        )
    get_tool_tags_admin_list_display.short_description = 'Associated tools'

    def get_version_tags_admin_list_display(self):
        return ", ".join(
            [
                u'{tool_name} for {platform_name}'.format(
                    tool_name=version.tool.name,
                    platform_name=version.supported_os.display_name,
                )
                for version in self.version_tag.all()
            ]
        )
    get_version_tags_admin_list_display.short_description = 'Associated versions'

    def get_tags_admin_list_display(self):
        return ", ".join(
            [tag.slug for tag in self.tags.all()]
        )
    get_tags_admin_list_display.short_description = 'Tags'

    def get_absolute_url(self):
        """
            Tell Django how to calculate the canonical URL for a Post object
            This method is necessary for the sitemap URL generation and will add
            `View on Site` option on the post object admin page

            Returns:
            An absolute URL for a post object
        """

        published_date_iso8601 = self.published_date.isoformat()[:10]

        return reverse(
            'webfrontend:blogpost',
            args=[
                published_date_iso8601,
                self.slug,
            ]
        )


post_save.connect(blogs_changed, sender=Post)
post_delete.connect(blogs_changed, sender=Post)
post_save.connect(purge_blog, sender=Post)
post_delete.connect(purge_blog, sender=Post)


class Comment(models.Model):
    """
        Model to represent the blog comments.
    """

    comment_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Comment Date'))
    email = models.CharField(
        max_length=256,
        verbose_name=_('Email'))
    name = models.CharField(
        max_length=256,
        verbose_name=_('Name'))
    title = models.CharField(
        max_length=512,
        verbose_name=_('Title'))
    content = models.TextField(
        verbose_name=_('Content'))
    approved = models.BooleanField(
        default=False,
        verbose_name=_('Approved'))
    post = models.ForeignKey(
        Post,
        verbose_name=_('Post'),
        related_name='comment',
        on_delete=models.CASCADE)

    def __str__(self):

        return self.title


post_save.connect(purge_blog, sender=Comment)
post_delete.connect(purge_blog, sender=Comment)
