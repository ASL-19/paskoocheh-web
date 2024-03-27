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


from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from markdownx.models import MarkdownxField
from .preferences_settings import PROMOIMAGE_PATH, TOOLTYPE_PATH, PLATFORM_PATH
from preferences.signals import texts_changed
from paskoocheh.mixins import ImageWithCachedDimensionsMixin
from paskoocheh.helpers import (
    get_hashed_filename,
    SingletonModel,
    validate_slug_strict,
    validate_platform_slug_strict,
)
from tools.signals import tools_changed
from webfrontend.caches.responses.signal_handlers import (
    purge_all,
    purge_index,
    purge_pages,
)
from django.core.validators import FileExtensionValidator
from django.db.models import JSONField


class GooglePlayApiPreference(SingletonModel):

    android_id = models.CharField(
        _('Android ID'),
        max_length=64,
        null=True,
        blank=True)
    google_user = models.CharField(
        _('Email Address'),
        max_length=128,
        null=True,
        blank=True)
    google_pass = models.CharField(
        _('Password'),
        max_length=128,
        null=True,
        blank=True)
    token = models.CharField(
        _('Token'),
        max_length=512,
        null=True,
        blank=True)

    class Meta:
        verbose_name = _(u'Google Play API')
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Google Play API Settings'


class PaskoochehAndroidPreference(SingletonModel):

    android_update_emails = models.TextField(
        _('Update Recipients (csv)'),
        max_length=64)

    class Meta:
        verbose_name = _(u'Android Apps')
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Android App Settings'


def get_tooltype_icon_upload_to(instance, filename):
    return u'{path}/{hashed_filename}'.format(
        path=TOOLTYPE_PATH,
        hashed_filename=get_hashed_filename(instance.icon.file)
    )


class ToolType(models.Model):
    """
        Type of tools model
    """

    name = models.CharField(
        max_length=256,
        verbose_name=_('Type Name'),
        null=False,
        blank=False)
    name_fa = models.CharField(
        max_length=256,
        verbose_name=_('Type Name in Farsi'),
        null=True,
        blank=False)
    name_ar = models.CharField(
        max_length=256,
        verbose_name=_('Type Name in Arabic'),
        null=True,
        blank=True)
    slug = models.SlugField(
        allow_unicode=False,
        max_length=20,
        verbose_name=_('Type URL slug'),
        default='',
        null=False,
        blank=False,
        validators=[validate_slug_strict])
    icon = models.FileField(
        upload_to=get_tooltype_icon_upload_to,
        validators=[FileExtensionValidator(['jpg', 'png', 'svg'])],
        verbose_name=_('Tool Type Icon'),
        null=True,
        blank=True)

    @property
    def admin_thumbnail(self):
        """
            Return an image to be displayed in admin panel

            Returns:
            An html to image icon if exists or a text of no image otherwise.
        """

        if self.icon:
            return mark_safe("<img src='{}' height='100' />".format(self.icon.url))
        else:
            return "( No Image )"

    def __str__(self):
        """
            Returns unicode representation of Tool Type
        """

        return self.name


post_save.connect(purge_all, sender=ToolType)
post_delete.connect(purge_all, sender=ToolType)
post_save.connect(tools_changed, sender=ToolType)
post_delete.connect(tools_changed, sender=ToolType)


def get_promoimage_image_upload_to(instance, filename):
    return u'{path}/{hashed_filename}'.format(
        path=PROMOIMAGE_PATH,
        hashed_filename=get_hashed_filename(instance.image.file)
    )


class PromoImage(models.Model, ImageWithCachedDimensionsMixin):
    """
        Promo Image model
        Store images of the tools
    """

    BEHAVIOUR_CHOICES = (
        ('Download APK overlay', 'AndroidOverlay'),
    )
    image = models.ImageField(
        upload_to=get_promoimage_image_upload_to,
        verbose_name=_('Promo Image'))
    title = models.CharField(
        max_length=1000,
        null=False,
        blank=False,
        verbose_name=_('Image title'))
    link = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name=_('Link URL'))
    new_window = models.BooleanField(
        default=True,
        verbose_name=_('Open in new window?'))
    behaviour = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        choices=BEHAVIOUR_CHOICES,
        verbose_name='Custom Behavior for Promo Image')
    language = models.CharField(
        max_length=2,
        default=settings.LANGUAGE_SUPPORTED_DEFAULT,
        choices=settings.LANGUAGE_SUPPORTED_CHOICES,
        null=False,
        blank=False,
        verbose_name=_('Language'))
    publish = models.BooleanField(
        default=True)
    width = models.IntegerField(
        null=True,
        default=0)
    height = models.IntegerField(
        null=True,
        default=0)
    order = models.IntegerField(
        default=1,
        verbose_name=_('Order'))

    def save(self, *args, **kwargs):
        # From ImageWithCachedDimensionsMixin
        self.save_image_dimensions()

        super(PromoImage, self).save(*args, **kwargs)

    def __str__(self):
        """
            Returns unicode representation of Promo Images
        """

        return self.title

    @property
    def admin_thumbnail(self):
        """
            Return an image to be displayed in admin panel

            Returns:
            An html to image if exists or a text of no image otherwise.
        """

        if self.image:
            return mark_safe("<img src='{}' height='100' />".format(self.image.url))
        else:
            return "( No Image )"

    class Meta(object):

        ordering = [
            'order'
        ]


post_save.connect(purge_index, sender=PromoImage)
post_delete.connect(purge_index, sender=PromoImage)


class Text(models.Model):
    """
        This class defines an API model to provide texts such as privacy policy,
        About, Contact information, etc.

        The class has provision for 3 languages for each text.
    """

    language = models.CharField(
        max_length=2,
        default=settings.LANGUAGE_SUPPORTED_DEFAULT,
        choices=settings.LANGUAGE_SUPPORTED_CHOICES,
        null=False,
        blank=False,
        verbose_name=_('Language'))
    last_modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Time'))
    about = MarkdownxField(
        null=True,
        blank=True,
        verbose_name=_('About Paskoocheh'))
    contact_email = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_('Contact Email'))
    privacy_policy = MarkdownxField(
        null=True,
        blank=True,
        verbose_name=_('Privacy Policy'))
    terms_and_privacy = MarkdownxField(
        null=True,
        blank=True,
        verbose_name=_(u'Terms of Service and Privacy Policy'),
        help_text=u'Note: This field is deprecated as terms of service and privacy policy texts have been separated into two pages')
    terms_of_service = MarkdownxField(
        null=True,
        blank=True,
        verbose_name=_('Terms of Service'))
    telegraph_footer = MarkdownxField(
        null=True,
        blank=True,
        verbose_name=_('FAQ Page Footer'))
    # TODO: Set default to False once production DB has been migrated
    publishable = models.BooleanField(
        null=False,
        default=True,
        verbose_name=_('Publish'),
        help_text='Check this box to publish post.')

    def __str__(self):

        return self.get_language_display()

    class Meta:

        verbose_name_plural = _('Web Texts')


post_save.connect(texts_changed, sender=Text)
post_save.connect(purge_pages, sender=Text)
post_delete.connect(purge_pages, sender=Text)


def get_platform_icon_upload_to(instance, filename):
    return u'{path}/{hashed_filename}'.format(
        path=PLATFORM_PATH,
        hashed_filename=get_hashed_filename(instance.icon.file)
    )


class Platform(models.Model):
    """
        Defines different platforms that apps are developed for
    """
    PLATFORM_CATEGORY_CHOICES = (
        ('d', 'Desktop'),
        ('m', 'Mobile'),
        ('w', 'Web')
    )

    name = models.CharField(
        max_length=64,
        null=False,
        blank=False,
        verbose_name=_('Platform Name'))
    display_name_fa = models.CharField(
        max_length=64,
        null=False,
        blank=False,
        verbose_name=_('Platform Name in Farsi'))
    display_name_ar = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name=_('Platform Name in Arabic'))
    display_name = models.CharField(
        max_length=64)
    slug_name = models.CharField(
        max_length=64,
        validators=[validate_platform_slug_strict],
        help_text='<strong>WARNING: Please arrange with the development team before adding/changing this value.</strong>')
    category = models.CharField(
        max_length=1,
        choices=PLATFORM_CATEGORY_CHOICES,
        default='d')
    icon = models.FileField(
        upload_to=get_platform_icon_upload_to,
        validators=[FileExtensionValidator(['jpg', 'png', 'svg'])],
        verbose_name=_('Tool Type Icon'),
        null=True,
        blank=True)

    def __str__(self):
        return self.display_name


post_save.connect(purge_all, sender=Platform)
post_delete.connect(purge_all, sender=Platform)
post_save.connect(tools_changed, sender=Platform)
post_delete.connect(tools_changed, sender=Platform)


class GeneralPreference(SingletonModel):

    from_email = models.CharField(
        max_length=254,
        null=False,
        blank=False,
        verbose_name=_('From Email'),
        help_text=_('The email address from which notification emails such as support or contact update emails will be sent.<br /><strong>WARNING: Please arrange with SysOps before changing these values.</strong>'))

    support_recipient_emails = models.TextField(
        _('Support Ticket Recipients (comma separated)'),
        max_length=1024,
        help_text=_('The email address(es) to which notification emails such as support or contact update emails will be sent.<br /><strong>WARNING: Please arrange with SysOps before changing these values.</strong>'))

    support_email = models.CharField(
        max_length=254,
        null=True,
        blank=False,
        verbose_name=_('Support Email Address'))

    twitter = models.CharField(
        max_length=254,
        null=True,
        blank=True,
        verbose_name=_('Twitter'))

    facebook = models.CharField(
        max_length=254,
        null=True,
        blank=True,
        verbose_name=_('Facebook'))

    instagram = models.CharField(
        max_length=254,
        null=True,
        blank=True,
        verbose_name=_('Instagram'))

    telegram = models.CharField(
        max_length=254,
        null=True,
        blank=True,
        verbose_name=_('Telegram'))

    class Meta:
        verbose_name = _(u'General Settings')
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'General Settings'


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name=_('Tag Name'))
    slug = models.SlugField(
        allow_unicode=False,
        max_length=20,
        verbose_name=_('Tag slug'),
        default='',
        null=False,
        blank=False,
        validators=[validate_slug_strict])

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.name


class AndroidDeviceProfile(models.Model):

    DEVICE_STATUS_CHOICES = (
        ('ready', 'Ready'),  # ready to update device.properties via cron
        ('added', 'Added'),  # added system properties only to device.properties
        ('completed', 'Completed'),  # completed all device properties in device.properties
        ('not_found', 'Not Found'),  # device properties could not be fetched
    )

    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name=_('Name'))
    codename = models.SlugField(
        allow_unicode=False,
        max_length=39,
        verbose_name=_('Code Name'),
        null=False,
        blank=False)
    properties = JSONField(
        null=True,
        blank=True,
        verbose_name=_('Device Properties (JSON)'))
    status = models.CharField(
        max_length=32,
        choices=DEVICE_STATUS_CHOICES,
        default='completed')

    class Meta:
        verbose_name = _('Android Device Profile')
        verbose_name_plural = _('Android Device Profiles')

    def __str__(self):
        return u'{} | {}'.format(self.codename, self.name)
