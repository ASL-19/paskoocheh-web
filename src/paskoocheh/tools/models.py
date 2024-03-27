# -*- coding: utf-8 -*-
# Paskoocheh - A tool marketplace for Iranian

# Copyright (C) 2024 ASL19 Organization

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import bleach
import re
import logging
from jdatetime import datetime as jdatetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation
)
from django.conf import settings
from django.db import models
from django.db.models.signals import (
    post_save,
    post_delete,
)
from django.utils import timezone
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from markdownx.models import MarkdownxField
from preferences.models import (
    ToolType,
    Platform,
    Tag,
    AndroidDeviceProfile,
)
from .signals import (
    faqs_changed,
    guides_changed,
    tools_changed,
    version_code_changed,
    version_code_deleted,
)
from .tools_settings import (
    IMAGE_PATH,
    TOOLS_PATH,
    VIDEO_PATH,
    SPLITS_PATH,
)
from pyskoocheh import crypto
from paskoocheh.mixins import ImageWithCachedDimensionsMixin
from paskoocheh.helpers import (
    SingletonModel,
    get_hashed_filename,
    validate_slug_strict)
from webfrontend.caches.responses.signal_handlers import (
    purge_faq,
    purge_guide,
    purge_info_tool_version,
    purge_tutorial,
)

logger = logging.getLogger('tools')


# TODO: not used that in the code yet
class VersionManager(models.Manager):
    """
    Version Manager model
    """
    def get_queryset(self):
        """
        get queryset
        """
        return super(VersionManager, self).get_queryset().filter("supported_os")


def get_image_image_upload_to(instance, filename):
    return u'{path}/{hashed_filename}'.format(
        path=IMAGE_PATH,
        hashed_filename=get_hashed_filename(instance.image.file)
    )


class Image(models.Model, ImageWithCachedDimensionsMixin):
    """
        Image model for screen shots and logos
        Store images of the tools
    """
    IMAGE_TYPE_CHOICES = (
        ('logo', _('LOGO')),
        ('screenshot', _('SCREENSHOT')),
        ('header', _('HEADER')),
    )

    last_modified = models.DateTimeField(
        verbose_name=_('Last modified time'),
        auto_now=True)
    image = models.ImageField(
        upload_to=get_image_image_upload_to,
        verbose_name=_('Image File'))
    image_type = models.CharField(
        default='logo',
        max_length=50,
        choices=IMAGE_TYPE_CHOICES,
        verbose_name=_('Image Type'))
    limit = \
        models.Q(app_label='tools', model='tool') | \
        models.Q(app_label='tools', model='version')

    # The below three properties are needed for Generic Foreign Key implementation
    content_type = models.ForeignKey(
        ContentType,
        related_name='images',
        on_delete=models.CASCADE,
        limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    width = models.IntegerField(
        null=True,
        default=0)
    height = models.IntegerField(
        null=True,
        default=0)
    should_display_full_bleed = models.BooleanField(
        default=False,
        verbose_name=_('Should display full-bleed'),
        help_text=_('If checked, and if the image is a logo image, clients should display it full-bleed (without any padding). Full-bleed images should have a coloured background and internal padding, or a transparent background and internal padding. Has no effect on non-logo images.'))
    order = models.IntegerField(
        default=0,
        verbose_name=_('Order'))
    publish = models.BooleanField(
        default=True,
        verbose_name=_('Publish'))
    language = models.CharField(
        blank=True,
        null=True,
        max_length=2,
        default=None,
        choices=settings.LANGUAGE_SUPPORTED_CHOICES,
        verbose_name=_('Language'),
        help_text=_('If set, this image will only appear in the specified language. Otherwise, it will appear in all languages.'))

    @property
    def object_name(self):
        """
            A name to represent the reviewed object on
            admin panel.

            Returns:
            A string containing the reviewd object type
        """

        return str(self.content_object)

    def save(self, *args, **kwargs):
        # From ImageWithCachedDimensionsMixin
        self.save_image_dimensions()

        super(Image, self).save(*args, **kwargs)

    def get_thumbnail_admin_list_display(self):
        if self.image:
            return mark_safe('<img src="{}" height="100" />'.format(self.image.url))
        else:
            return '( No Image )'
    get_thumbnail_admin_list_display.short_description = 'Thumbnail'

    class Meta:

        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ['image_type']


class Tool(models.Model):
    """
    Tool model
    """

    last_modified = models.DateTimeField(
        verbose_name=_('Last modified time'),
        auto_now=True)
    created = models.DateTimeField(
        verbose_name=_('Created time'),
        null=True,
        auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Author"),
        related_name=('tools'))
    name = models.CharField(
        max_length=50,
        help_text=_('This is just a latin name for admin panel only'),
        verbose_name=_('Tool name'))
    slug = models.SlugField(
        max_length=75,
        unique=True,
        help_text=_('This slug will show in the URL for this app'),
        verbose_name=_('Tool slug'))
    last_update = models.DateTimeField(
        auto_now=True,
        help_text='Last time the tool was updated')
    trusted = models.BooleanField(
        default=False,
        help_text=_('Whether you trust the tool\'s source'),
        verbose_name=_('Trusted Source'))
    featured = models.BooleanField(
        default=False,
        help_text=_('Is this tool featured'),
        verbose_name=_('Featured Tool'))
    opensource = models.BooleanField(
        null=False,
        default=False,
        verbose_name=_('Open source'))
    source = models.URLField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name=_('Source url on Github or Bitbucket'))
    primary_tooltype = models.ForeignKey(
        ToolType,
        on_delete=models.PROTECT,
        related_name='primary_tools',
        verbose_name=_('Primary Tool Type'))
    tooltype = models.ManyToManyField(
        ToolType,
        related_name='tools',
        verbose_name=_('Tool Type'))

    # Links and social networking fields
    website = models.URLField(
        max_length=1000,
        verbose_name=_('Main website of the tool'),
        null=False,
        unique=True)
    facebook = models.URLField(
        max_length=1000,
        verbose_name=_('Facebook URL'),
        null=True,
        blank=True)
    twitter = models.URLField(
        max_length=1000,
        verbose_name=_('Twitter URL'),
        null=True,
        blank=True)
    rss = models.URLField(
        verbose_name=_('Feed URL'),
        null=True,
        blank=True)
    blog = models.URLField(
        verbose_name=_('Link of the company blog'),
        null=True,
        blank=True)
    contact_email = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name=_('Support email address'))
    contact_url = models.URLField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name=_('Support url on the company website'))
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("Tags"),
        related_name=('tools'),
        blank=True)
    publishable = models.BooleanField(
        null=False,
        default=False,
        verbose_name=_('Publish'),
        help_text='Check this box to publish post.')
    images = GenericRelation(Image)

    def get_app_name(self):
        name = re.compile(r'\W+', re.U)
        return name.sub('', self.name.lower())

    def __str__(self):
        """
            Return unicode representation of Tool
        """

        return u'{0}'.format(self.name)

    class Meta(object):
        """
            Database metadata class
        """

        verbose_name = _('Tool')
        verbose_name_plural = _('Tools')


post_save.connect(tools_changed, sender=Tool)
post_delete.connect(tools_changed, sender=Tool)
post_save.connect(purge_info_tool_version, sender=Tool)
post_delete.connect(purge_info_tool_version, sender=Tool)


def get_video_upload_to(instance, filename):
    return u'{path}/{hashed_filename}'.format(
        path=VIDEO_PATH,
        hashed_filename=get_hashed_filename(instance.video.file)
    )


def update_video_help_text_snippet(file_path='[file_path]'):
    return '''
            <b>To insert the uploaded video into the post, save and then use the following snippet:</b>

            <code>
            <pre>&lt;div class="embedded-video"&gt;
            &lt;video class="g-video-viewport" controls&gt;
            &lt;source src="{media_url}{file_path}" type="video/mp4"&gt;
            &lt;p&gt;Your browser does not support HTML5 video. Here is a &lt;a href="{media_url}{file_path}"&gt;link to the video&lt;/a&gt;.&lt;/p&gt;
            &lt;/video&gt;
            &lt;/div&gt;</pre>
            </code>
        '''.format(media_url=settings.MEDIA_URL,
                   file_path=file_path)


class HomeFeaturedTool(SingletonModel):

    tool = models.ForeignKey(
        Tool,
        verbose_name=_('Tool'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL)

    promo_text = models.CharField(
        max_length=250,
        verbose_name=_('Promo text'),
        blank=True)

    class Meta:
        verbose_name = _(u'Homepage Featured Tool')
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.tool:
            return f'Homepage Featured Tool: {self.tool.name}'
        return 'Homepage Featured Tool: Unspecified'


class Info(models.Model):
    """
        Info model
        This model cannot be embedded in Tool model mostly because of internationalization
    """

    last_modified = models.DateTimeField(
        verbose_name=_('Last modified time'),
        auto_now=True)
    tool = models.ForeignKey(
        Tool,
        related_name='infos',
        verbose_name=_('Corresponding tool'),
        on_delete=models.CASCADE)
    language = models.CharField(
        max_length=2,
        default=settings.LANGUAGE_SUPPORTED_DEFAULT,
        choices=settings.LANGUAGE_SUPPORTED_CHOICES,
        verbose_name=_('Language'))
    name = models.CharField(
        max_length=100,
        null=False,
        unique=True,
        verbose_name=_('Language-specific name'),
        help_text=_('Name of the tool in the corresponding language'))
    company = models.CharField(
        max_length=100,
        verbose_name=_('Company name'))
    description = MarkdownxField(
        null=True,
        blank=True,
        verbose_name=_('Description'),
        help_text=_('Description of tool, max 2000 character'))
    seo_description = models.TextField(
        verbose_name=_('SEO description'),
        blank=True,
        help_text=_('The descriptive text displayed underneath a headline in search engine results.'))
    # TODO: Set default to False once production DB has been migrated
    publishable = models.BooleanField(
        null=False,
        default=True,
        verbose_name=_('Publish'),
        help_text='Info is publishable (can appear on site)')

    def __str__(self):
        """
            Return unicode representation of Info
        """

        return u'{0}'.format(self.name)

    def get_tool_name(self):
        return self.tool.name
    get_tool_name.short_description = 'Corresponding tool'
    get_tool_name.admin_order_field = 'tool__name'

    class Meta(object):

        unique_together = (
            'tool',
            'language')
        verbose_name = _('Information about the tool')
        verbose_name_plural = _('Tools information')


post_save.connect(tools_changed, sender=Info)
post_delete.connect(tools_changed, sender=Info)

post_save.connect(purge_info_tool_version, sender=Info)
post_delete.connect(purge_info_tool_version, sender=Info)


def update_filename(instance, filename):
    """
        A method for upload_to for the version

        Args:
        instance: the instance of the Version
        filename: the filename based on the tool name

        Returns:
        filename including the path
    """

    path = TOOLS_PATH
    forbidden_extensions = ['exe', 'ade', 'adp', 'bat',
                            'chm', 'cmd', 'com', 'cpl',
                            'exe', 'hta', 'ins', 'isp',
                            'jar', 'jse', 'lib', 'lnk',
                            'mde', 'msc', 'msp', 'mst',
                            'pif', 'scr', 'sct', 'shb',
                            'sys', 'vb', 'vbe', 'vbs',
                            'vxd', 'wsc', 'wsf', 'wsh']
    if instance.uploaded_file == '':
        return u''
    tool_name = re.compile(r'\W+', re.U)
    appname = tool_name.sub('', instance.version.tool.name.lower())
    extension = instance.uploaded_file.name.split('.')[-1].lower()
    if extension in forbidden_extensions:
        extension = 'abc'
    if '.tar.bz2' in instance.uploaded_file.name:
        extension = 'tar.bz2'
    if '.tar.gz' in instance.uploaded_file.name:
        extension = 'tar.gz'
    if '.tar.xz' in instance.uploaded_file.name:
        extension = 'tar.xz'

    name = appname + '/' + instance.version.supported_os.slug_name.lower() + '/' + \
        str(instance.version_code) + '/' + \
        appname + '-' + instance.version.supported_os.slug_name.lower() + '.' + \
        extension

    file_name = os.path.join(path, name)

    if instance.uploaded_file.storage.exists(file_name):
        instance.uploaded_file.storage.delete(file_name)

    return file_name


class Version(models.Model):
    """
        Version model
        Include the information about different version of each tool
    """

    last_modified = models.DateTimeField(
        verbose_name=_('Last modified time'),
        auto_now=True)
    created = models.DateTimeField(
        verbose_name=_('Created time'),
        null=True,
        auto_now_add=True)
    tool = models.ForeignKey(
        Tool,
        related_name='versions',
        verbose_name=_('Corresponding tool'),
        on_delete=models.CASCADE)
    version_number = models.CharField(
        max_length=128,
        null=False,
        verbose_name=_('Tool version number'),
        help_text=_('Each version might have different number, when'
                    ' an update happens, this field must change or'
                    ' the user will not receive a notification'))
    supported_os = models.ForeignKey(
        Platform,
        related_name=('versions'),
        verbose_name=_('Platforms'),
        on_delete=models.CASCADE)
    release_date = models.DateTimeField(
        verbose_name=_('Actual release date from publisher'),
        default=timezone.now)
    release_jdate = models.CharField(
        max_length=32,
        verbose_name=_('Release date in Jalali'))
    download_url = models.CharField(
        blank=True,
        max_length=1000,
        verbose_name=_('Download url'))
    release_url = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name=_('Link to the release news if any'))
    # Below are Android Specific fields
    package_name = models.CharField(
        blank=True,
        null=True,
        max_length=1000,
        verbose_name=_('Android-specific Package Name'))
    auto_update = models.BooleanField(
        blank=False,
        null=False,
        default=True,
        verbose_name=_('Android-specific Automatic Update'))
    permissions = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Android-specific App Permissions (CSV)'))
    images = GenericRelation(Image)
    guide_url = models.CharField(
        blank=True,
        max_length=1000,
        default='',
        verbose_name=_('Guide url'))
    faq_url = models.CharField(
        blank=True,
        max_length=1000,
        default='',
        verbose_name=_('FAQ url'))
    # TODO: Set default to False once production DB has been migrated
    publishable = models.BooleanField(
        null=False,
        default=True,
        verbose_name=_('Publish'),
        help_text='Check this box to publish post.')
    video = models.FileField(
        upload_to=get_video_upload_to,
        null=True,
        blank=True,
        verbose_name=_('Video File'),
        help_text='If set while Video Link is also set, the uploaded video will not be displayed as the embedded video (Video Link) is the default.')
    video_link = models.URLField(
        null=True,
        blank=True,
        verbose_name=_('Video Link'))
    is_bundled_app = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        verbose_name=_('Android-specific Bundled App'))

    @property
    def delivery_email(self):
        """
            Delivery email - auto-generated
        """

        appname = self.tool.get_app_name()

        email = (
            appname +
            '-' +
            self.supported_os.slug_name.lower() +
            '@' +
            settings.PLATFORM +
            '.' +
            settings.TOP_LEVEL_DOMAIN
        )

        return u'{}'.format(email)

    def save(self, *args, **kwargs):
        self.release_jdate = (
            jdatetime.fromgregorian(datetime=self.release_date)
            .strftime(u'%Y/%m/%d')
            .replace(u'/0', u'/')  # Remove leading zeroes
        )
        super(Version, self).save(*args, **kwargs)

    def get_tool_name(self):
        return self.tool.name

    get_tool_name.short_description = 'Tool'
    get_tool_name.admin_order_field = 'tool__name'

    def get_tool_id(self):
        return self.tool.id

    get_tool_id.short_description = 'Tool ID'
    get_tool_id.admin_order_field = 'tool__id'

    def get_supported_os_name(self):
        return self.supported_os.display_name
    get_supported_os_name.short_description = 'Platform'
    get_supported_os_name.admin_order_field = 'supported_os__display_name'

    def get_absolute_url(self):
        """
            Tell Django how to calculate the canonical URL for a Version object
            This method is necessary for the sitemap URL generation and will add
            `View on Site` option on the version object admin page

            Returns:
            A version URL
        """

        return reverse(
            'webfrontend:toolversion',
            args=[
                self.tool.id,
                self.supported_os.slug_name,
            ]
        )

    def __str__(self):
        """
        Return unicode representation of Version
        """

        return u'{0} for {1} : {2}'.format(self.tool.name,
                                           self.supported_os.slug_name,
                                           self.version_number)

    class Meta(object):

        unique_together = (
            ('tool', 'supported_os'),
        )
        verbose_name = _('Version')
        verbose_name_plural = _('Versions')


post_save.connect(purge_info_tool_version, sender=Version)
post_delete.connect(purge_info_tool_version, sender=Version)


def split_file_upload_location(instance, filename):
    """
        A method for upload_to for the split file for Android bundled apps

        Args:
        instance: the instance of the Android split file
        filename: the filename of the split file

        Returns:
        the split file location including the path
    """

    path = TOOLS_PATH
    name = instance.create_split_filename()

    split_file_location = os.path.join(path, name)

    if instance.split_file.storage.exists(split_file_location):
        instance.split_file.storage.delete(split_file_location)

    return split_file_location


class VersionCode(models.Model):
    """
    Version Code model
    Includes the information about different version codes for each version code of tools
    """
    last_modified = models.DateTimeField(
        verbose_name=_('Last modified time'),
        auto_now=True)
    created = models.DateTimeField(
        verbose_name=_('Created time'),
        null=True,
        auto_now_add=True)
    version = models.ForeignKey(
        Version,
        related_name='version_codes',
        on_delete=models.CASCADE)
    version_code = models.IntegerField(default=0)
    uploaded_file = models.FileField(
        blank=True,
        null=True,
        upload_to=update_filename,
        verbose_name=_('Release Binary'))
    checksum = models.CharField(
        blank=True,
        null=True,
        max_length=1000,
        verbose_name=_('Checksum for release binary'))
    size = models.IntegerField(
        blank=True,
        default=0,
        verbose_name=_('Size of download in bytes'))
    signature = models.CharField(
        blank=True,
        null=True,
        max_length=1024,
        verbose_name=_('Binary Signature'))
    sig_file = models.FileField(
        blank=True,
        null=True,
        verbose_name=_('Signature File'))
    devices = models.ManyToManyField(
        AndroidDeviceProfile,
        verbose_name="Devices",
        related_name="device_version_codes",
        blank=True)

    class Meta(object):
        verbose_name = _('Version Code')
        verbose_name_plural = _('Version Codes')

    def __str__(self):
        return "{0} | tool: {1} | version: {2}".format(self.version_code,
                                                       self.version.tool.name, self.version.version_number)

    def get_platform_name(self):
        return self.version.supported_os.display_name

    @property
    def s3_key(self):
        """
            S3 Key - auto-generated
        """

        s3key = self.create_filename()
        if len(s3key) > 0:
            s3key = f'/{settings.TOOLS_PREFIX}' + s3key

        return u'{}'.format(s3key)

    def create_filename(self):
        """
            Create file name based on the app name
            including the path name
        """
        forbidden_extensions = ['exe', 'ade', 'adp', 'bat',
                                'chm', 'cmd', 'com', 'cpl',
                                'exe', 'hta', 'ins', 'isp',
                                'jar', 'jse', 'lib', 'lnk',
                                'mde', 'msc', 'msp', 'mst',
                                'pif', 'scr', 'sct', 'shb',
                                'sys', 'vb', 'vbe', 'vbs',
                                'vxd', 'wsc', 'wsf', 'wsh']
        if self.uploaded_file == '':
            return u''

        appname = self.version.tool.get_app_name()
        extension = self.uploaded_file.name.split('.')[-1].lower()
        if extension in forbidden_extensions:
            extension = 'abc'
        if '.tar.bz2' in self.uploaded_file.name:
            extension = 'tar.bz2'
        if '.tar.gz' in self.uploaded_file.name:
            extension = 'tar.gz'
        if '.tar.xz' in self.uploaded_file.name:
            extension = 'tar.xz'

        filename = appname + '/' + self.version.supported_os.slug_name.lower() + '/' + \
            str(self.version_code) + '/' + \
            appname + '-' + self.version.supported_os.slug_name.lower() + '.' + \
            extension

        return filename

    def save(self, *args, **kwargs):

        # To restrict creation of more than one Version Code per specific Version (non-android platforms)
        if self.version.supported_os.slug_name != 'android' and VersionCode.objects.filter(version=self.version) and self.pk is None:
            from django.core.exceptions import ValidationError
            raise ValidationError(
                u'Version Code for this Version already exists!'
            )

        if self.uploaded_file and settings.BUILD_ENV != 'local':

            extension = self.uploaded_file.name.split('.')[-1].lower()
            has_splits = self.version.is_bundled_app

            # The Updater (tools.updater) has an intermediate version save() operation for bundled apps
            # to temporarily save the base apk before bundling all version splits + that base apk into
            # a zip file. So to optimize the performance of the Updater, these calculations shall not
            # go through except for unbundled apps with an apk extension OR bundled apps with a zip
            # extension to calculate the signature and checksum for the final release file only.
            if ((has_splits is True and extension == 'zip') or
                    (has_splits is False and extension == 'apk') or
                    (has_splits is False and extension == 'pdf')):
                signer = crypto.SignatureManager(
                    settings.PGP_PRIVATE_KEY, settings.PGP_KEY_PASSWORD)

                try:
                    logger.info(f"Calculating signature for [{self.uploaded_file.name}]...")
                    self.signature = signer.calc_signature(self.uploaded_file)
                except Exception as e:
                    logger.error(f"Error calculating signature of the file: ({str(e)})")

                try:
                    logger.info(f"Computing checksum for [{self.uploaded_file.name}]...")
                    self.checksum = signer.calc_compute_checksum(
                        self.uploaded_file)
                except Exception as e:
                    logger.error(f"Error calculating checksum of the file: ({str(e)})")

        super(VersionCode, self).save(*args, **kwargs)


post_save.connect(version_code_changed, sender=VersionCode)
post_delete.connect(version_code_deleted, sender=VersionCode)
post_save.connect(purge_info_tool_version, sender=VersionCode)
post_delete.connect(purge_info_tool_version, sender=VersionCode)


class AndroidSplitFile(models.Model):
    version = models.ForeignKey(
        Version,
        on_delete=models.CASCADE)
    split_file = models.FileField(
        upload_to=split_file_upload_location,
        null=False,
        blank=False)
    size = models.IntegerField(
        blank=True,
        default=0,
        verbose_name=_('Size (bytes)'))
    # TODO: Needs to be removed
    devices = models.ManyToManyField(
        AndroidDeviceProfile,
        verbose_name=_("Devices"),
        related_name=('splits'),
        blank=False)
    tool_version_code = models.ForeignKey(
        VersionCode,
        related_name='android_split_files',
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    @property
    def s3_key(self):
        """
            S3 Key - auto-generated
        """
        s3key = '-'
        if self.split_file and len(s3key) > 0:
            s3key = '/' + TOOLS_PATH + self.create_split_filename()

        return s3key

    def create_split_filename(self):
        """
            Create split file name based on the split file name
            including the path name
        """

        appname = self.version.tool.get_app_name()
        uploaded_filename = self.split_file.name.split('/')[-1].lower()
        filename = appname + '/' + self.version.supported_os.slug_name.lower() + '/' + \
            str(self.tool_version_code.version_code) + \
            '/' + SPLITS_PATH + uploaded_filename

        return filename

    def __str__(self):
        """
        Return unicode representation of SplitFile
        """

        return u'Split file [{}] for version [{}]'.format(self.split_file.name, self.version)

    class Meta(object):
        """
            Database metadata class
        """

        verbose_name = _('Split File')
        verbose_name_plural = _('Split Files')


class StepModel(models.Model):
    """
        Step model
        An abstruct class to provide a base for steps (Headline, Body) model that
        FAQ or Guide like models can use.
    """

    last_modified = models.DateTimeField(
        verbose_name=_('Last modified time'),
        auto_now=True)
    version = models.ForeignKey(
        Version,
        null=True,
        blank=True,
        verbose_name=_('Corresponding version'),
        on_delete=models.SET_NULL)
    language = models.CharField(
        max_length=2,
        default=settings.LANGUAGE_SUPPORTED_DEFAULT,
        choices=settings.LANGUAGE_SUPPORTED_CHOICES,
        verbose_name=_('Language'))
    headline = models.CharField(
        max_length=1000,
        null=False)
    body = MarkdownxField(
        null=False,
        blank=False)
    order = models.IntegerField(
        default=1,
        verbose_name=_('Order'))
    # TODO: Set default to False once production DB has been migrated
    publishable = models.BooleanField(
        null=False,
        default=True,
        verbose_name=_('Publish'),
        help_text='Is publishable (can appear on site)')

    def clean_headline(self):
        self.headline = bleach.clean(self.cleaned_data.get('headline', False))

    def clean_body(self):
        self.body = bleach.clean(self.cleaned_data.get('headline', False))

    def __str__(self):
        if self.version is not None:
            return u'{0} : {1} '.format(self.version.tool.name, self.headline)
        else:
            return str(self.headline)

    class Meta(object):

        ordering = [
            'version',
            'order']
        abstract = True


class Faq(StepModel):
    """
        Faq model
        Contains information about frequently asked questions for each tool
        When a Tool is deleted from the Tool Table we want all its faq records to be deleted as well
        and hence we will leave the default on_delete=cascade to be the case.
    """

    tool = models.ForeignKey(
        Tool,
        related_name='faqs',
        verbose_name=_('Corresponding tool'),
        on_delete=models.CASCADE)
    click_count = models.IntegerField(
        default=0,
        verbose_name=_('Click count'))
    video = models.FileField(
        upload_to=get_video_upload_to,
        null=True,
        blank=True,
        verbose_name=_('Video File'),
        help_text='Once the file to be uploaded has been saved, an HTML code snippet will be provided.')

    def get_tool_name(self):
        return self.tool.name
    get_tool_name.short_description = 'Corresponding tool'
    get_tool_name.admin_order_field = 'tool__name'

    def get_version_name(self):
        if self.version:
            return str(self.version)
        else:
            return None
    get_version_name.short_description = 'Corresponding version'
    get_version_name.admin_order_field = 'version__tool__name'

    def save(self, *args, **kwargs):
        if self.video:
            try:
                field = self._meta.get_field('video')
                field.help_text = update_video_help_text_snippet(self.video)
            except Exception:
                pass
        super(Faq, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
            Tell Django how to calculate the canonical URL for a Guide object
            This method is necessary for the sitemap URL generation and will add
            a `View on Site` option on the guide object admin page

            Returns:
            An absolute URL for a guide object
        """

        if self.version:
            viewname = 'webfrontend:toolversionfaq'
            args = [
                self.tool.id,
                self.version.supported_os.slug_name,
                self.id,
            ]
        elif self.tool:
            viewname = 'webfrontend:toolfaq'
            args = [
                self.tool.id,
                self.id,
            ]

        return reverse(
            viewname,
            args=args,
        )

    class Meta(object):
        """
            Database metadata class
        """

        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')


Faq._meta.get_field('headline').verbose_name = 'Question'
Faq._meta.get_field('body').verbose_name = 'Answer'
post_save.connect(faqs_changed, sender=Faq)
post_delete.connect(faqs_changed, sender=Faq)
post_save.connect(purge_faq, sender=Faq)
post_delete.connect(purge_faq, sender=Faq)


class Guide(StepModel):
    """
        Step by Step guide for tools version
    """
    slug = models.SlugField(
        blank=True,
        null=True,
        max_length=20,
        allow_unicode=False,
        verbose_name=_(u'URL slug'),
        help_text=u'If this is set, you can append “#[slug]” to the amalgamated guide page URL to link to this step.',
        validators=[validate_slug_strict],
    )
    video = models.FileField(
        upload_to=get_video_upload_to,
        null=True,
        blank=True,
        verbose_name=_('Video File'),
        help_text='Once the file to be uploaded has been saved, an HTML code snippet will be provided.')

    def get_version_name(self):
        if self.version:
            return str(self.version)
        else:
            return None
    get_version_name.short_description = 'Corresponding version'
    get_version_name.admin_order_field = 'version__tool__name'

    def save(self, *args, **kwargs):
        if self.video:
            try:
                field = self._meta.get_field('video')
                field.help_text = update_video_help_text_snippet(self.video)
            except Exception:
                pass
        super(Guide, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
            Tell Django how to calculate the canonical URL for a Guide object
            This method is necessary for the sitemap URL generation and will add
            a `View on Site` option on the guide object admin page

            Returns:
            An absolute URL for a guide object
        """

        return reverse(
            'webfrontend:toolversionguide',
            args=[
                self.version.tool.id,
                self.version.supported_os.slug_name,
            ]
        )


Guide._meta.get_field('headline').verbose_name = 'Title'
Guide._meta.get_field('body').verbose_name = 'Description'
post_save.connect(guides_changed, sender=Guide)
post_delete.connect(guides_changed, sender=Guide)
post_save.connect(purge_guide, sender=Guide)
post_delete.connect(purge_guide, sender=Guide)


class Tutorial(models.Model):
    """
        Tutorial model
        This model is not being used in beta version
    """

    last_modified = models.DateTimeField(
        verbose_name=_('Last modified time'),
        auto_now=True)
    version = models.ForeignKey(
        Version,
        related_name='tutorials',
        verbose_name=_('Corresponding version'),
        on_delete=models.CASCADE)
    language = models.CharField(
        max_length=2,
        default=settings.LANGUAGE_SUPPORTED_DEFAULT,
        choices=settings.LANGUAGE_SUPPORTED_CHOICES,
        verbose_name=_('Language'))
    video = models.FileField(
        upload_to=get_video_upload_to,
        null=True,
        blank=True,
        verbose_name=_('Video File'),
        help_text='If set while Video Link is also set, the uploaded video will not be displayed as the embedded video (Video Link) is the default.')
    video_link = models.URLField(
        null=True,
        blank=True,
        verbose_name=_('Video Link'))
    title = models.CharField(
        max_length=1000,
        null=False,
        blank=False,
        default='',
        verbose_name=_('Title'))
    order = models.IntegerField(
        default=1,
        verbose_name=_('Order'))
    # TODO: Set default to False once production DB has been migrated
    publishable = models.BooleanField(
        null=False,
        default=True,
        verbose_name=_('Publish'),
        help_text='Check this box to publish post.')

    def __str__(self):
        """
        Return unicode representation of Tutorial
        """

        return u'tutorial for {0} language {1}'.format(str(self.version), str(self.language))

    def get_version_name(self):
        return str(self.version)
    get_version_name.short_description = 'Corresponding version'
    get_version_name.admin_order_field = 'version__tool__name'

    def get_absolute_url(self):
        """
            Tell Django how to calculate the canonical URL for a Tutorial object
            This method is necessary for the sitemap URL generation and will add
            a `View on Site` option on the tutorial object admin page

            Returns:
            An absolute URL for a tutorial object
        """

        return reverse(
            'webfrontend:toolversiontutorial',
            args=[
                self.version.tool.id,
                self.version.supported_os.slug_name,
                self.id,
            ]
        )

    class Meta(object):

        ordering = [
            'version',
            'order']
        verbose_name = _('Tutorial')
        verbose_name_plural = _('Tutorials')


post_save.connect(tools_changed, sender=Tutorial)
post_delete.connect(tools_changed, sender=Tutorial)
post_save.connect(purge_tutorial, sender=Tutorial)
post_delete.connect(purge_tutorial, sender=Tutorial)


"""
class ReportManager(models.Manager):
    def save(self, validated_data, **kwargs):
        report = self.model(validated_data, kwargs)
        report.save()
        return report

class Report(models.Model):
    SPEED_CHOICES = (
        ("64k", _("64K and below")),
        ("128k", _("128k")),
        ("512k", _("512k")),
        ("1M", _("1M")),
        ("2M", _("2M")),
        ("3-5M", _("3 to 6M")),
        ("6-9M", _("6 to 9M")),
        ("10M", _("10M and above")),
    )
    # this way you can use report.quality = Report.Slow
    Fail = 1
    Slow = 2
    Moderate = 3
    Fast = 4
    Super = 5
    QUALITY_CHOICES = (
        (Fail, _("Fail to work")),
        (Slow, _("Very slow with multiple disconnections")),
        (Moderate, _("Moderate")),
        (Fast, _("Sometimes Fast")),
        (Super, _("Very Fast")),
    )
    FACEBOOK_CHOICES = (
        (Fail, _("Fail to work")),
        (Slow, _("Images not loading")),
        (Moderate, _("Videos not loading")),
        (Fast, _("Normal surfing")),
        (Super, _("Very Fast")),
    )
    YOUTUBE_CHOICES = (
        (Fail, _("Fail to work")),
        (Slow, _("Only thumbnails are loading")),
        (Moderate, _("Videos loads but slow")),
        (Fast, _("Normal surfing")),
        (Super, _("Very Fast")),
    )
    last_modified = models.DateTimeField(
        verbose_name=_('Last modified time'),
        auto_now=True)
    # When a Tool is deleted from the Tool Table we want all its report records to be deleted
    # as well and hence we will leave the default on_delete=cascade to be the case.
    tool = models.ForeignKey(
        Tool,
        related_name="reports",
        verbose_name=_("Corresponding tool"))
    email = models.EmailField(null=True, blank=True, verbose_name=_("Email"))
    reported_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date of Report"))
    country = models.CharField(max_length=64, null=False, verbose_name=_("Country"))
    province = models.CharField(max_length=100, null=False, verbose_name=_("Province"))
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("City"))
    ISP = models.CharField(max_length=200, null=False, verbose_name=_("ISP"))
    speed = models.CharField(max_length=16, choices=SPEED_CHOICES, null=False,
                             verbose_name=_("Speed"))
    quality = models.PositiveIntegerField(choices=QUALITY_CHOICES, null=False,
                                          verbose_name=_("Quality"))
    facebook_quality = models.PositiveIntegerField(choices=FACEBOOK_CHOICES, null=True, blank=True,
                                                   verbose_name=_("Facebook Quality"))
    youtube_quality = models.PositiveIntegerField(choices=YOUTUBE_CHOICES, null=True, blank=True,
                                                  verbose_name=_("Youtube Quality"))
    os = models.CharField(max_length=100, null=True, blank=True,
                          verbose_name=_("Operating system"))
    antivirus = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Antivirus"))
    firewall = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Firewall"))
    comment = models.TextField(null=True, blank=True, verbose_name=_("Comment"))

    # userAgent fields
    user_agent = models.CharField(max_length=300, verbose_name=_("The whole user agent string"),
                                  null=True, blank=True)
    user_agent_device_family = models.CharField(max_length=64, null=True, blank=True,
                                                verbose_name=_("User agent device family"))
    user_agent_os_family = models.CharField(max_length=64, null=True, blank=True,
                                            verbose_name=_("User agent operating system family"))
    user_agent_os_version = models.CharField(max_length=32, null=True, blank=True,
                                             verbose_name=_("User agent operating system version"))
    user_agent_browser_family = models.CharField(max_length=64, null=True, blank=True,
                                                 verbose_name=_("User agent browser fmily"))
    user_agent_browser_version = models.CharField(max_length=32, null=True, blank=True)
    # boolean fields does not accept null, use NullBoleanField
    user_agent_is_mobile = models.NullBooleanField(null=True, blank=True,
                                                   verbose_name=_("Mobile?"))
    user_agent_is_tablet = models.NullBooleanField(null=True, blank=True,
                                                   verbose_name=_("Tablet?"))
    user_agent_is_touch = models.NullBooleanField(null=True, blank=True, verbose_name=_("Touch?"))
    user_agent_is_pc = models.NullBooleanField(null=True, blank=True, verbose_name=_("PC?"))
    user_agent_is_bot = models.NullBooleanField(null=True, blank=True, verbose_name=_("Bot?"))

    objects = ReportManager()

    def __str__(self):
        return u"{0} by {1}".format(self.tool.name, self.reported_date)

    class Meta(object):
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
"""


class TeamAnalysis(models.Model):
    """
        Team Analysis model
        Used to show team ratings, review, pros and cons for each tool
    """

    tool = models.OneToOneField(
        Tool,
        related_name='team_analysis',
        on_delete=models.CASCADE)
    review = models.TextField(
        null=True,
        blank=True)
    pros = models.TextField(
        null=True,
        blank=True)
    cons = models.TextField(
        null=True,
        blank=True)

    def __str__(self):
        return f'{str(self.tool)}'

    class Meta:
        verbose_name_plural = 'Team Analysis'


class CategoryAnalysis(models.Model):
    """
        Category Analysis model
        Used to rate each tool by category in team analysis
    """

    tool = models.ForeignKey(
        TeamAnalysis,
        related_name='team_categoryratings',
        on_delete=models.CASCADE)
    rating_category = models.ForeignKey(
        'stats.RatingCategory',
        on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        verbose_name=_('Star Rating'),
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)],
        default=5)

    def __str__(self):
        return f'{str(self.tool)} - {str(self.rating_category)}: {self.rating}'

    class Meta:
        verbose_name_plural = 'Category Analysis'
        unique_together = [
            ('tool', 'rating_category'),
        ]
