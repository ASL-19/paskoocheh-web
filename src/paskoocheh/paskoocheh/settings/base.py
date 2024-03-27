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

import os
import re
import sys
from datetime import timedelta

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

from strawberry.annotation import StrawberryAnnotation
from strawberry.field import StrawberryField
from gqlauth.settings_type import GqlAuthSettings, DjangoSetting

# True if IS_DEVELOPMENT environment variable is 'true'. This is used to disable
# some functionality (especially interactions with production components) in
# development
IS_DEVELOPMENT = (os.environ.get('IS_DEVELOPMENT') == 'true')

# True if using `python manage.py runserver` or `python manage.py runsslserver`
IS_DEVELOPMENT_SERVER = (len(sys.argv) > 1 and sys.argv[1] in ['runserver', 'runsslserver'])

# Get a reference to the main settings module (e.g. settings/development.py or
# settings/production.py) so that we can access its attributes
env_settings_module = sys.modules[os.environ["DJANGO_SETTINGS_MODULE"]]

try:
    env_settings = {
        'LOG_LEVEL': env_settings_module.LOG_LEVEL
    }
except AttributeError as exception_instance:
    exception_message = exception_instance.args[0].replace(
        "'module' object",
        env_settings_module.__name__
    )

    raise ImproperlyConfigured(exception_message)


# PASKOOCHEH OR ZANGA
PLATFORM = os.environ.get('PLATFORM')
TOP_LEVEL_DOMAIN = 'tech' if PLATFORM == 'zanga' else 'com'

# PATH CONFIGURATION
DJANGO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(DJANGO_DIR)
DB_USER = os.environ['DATABASE_USER']
DB_PASSWORD = os.environ['DATABASE_PASSWORD']
DB_HOST = os.environ['DATABASE_HOST']
DB_NAME = os.environ['DATABASE_NAME']
BUILD_ENV = os.environ['BUILD_ENV']
VERSION_NUM = os.environ.get('VERSION_NUM', 'NA')
BUILD_NUM = os.environ.get('BUILD_NUM', 'NA')
GIT_SHORT_SHA = os.environ.get('GIT_SHORT_SHA', 'NA')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
EMAIL_LIST_URL = os.environ.get('EMAIL_LIST_URL')
EMAIL_LIST_HIDDEN = os.environ.get('EMAIL_LIST_HIDDEN')

PGP_KEY_PASSWORD = os.environ.get('PGP_KEY_PASSWORD')

PGP_PRIVATE_KEY = os.environ.get('PGP_PRIVATE_KEY')

FRONT_WEB_URL = os.environ.get('NEXT_PUBLIC_WEB_URL', None)

GRECAPTCHA_INVISIBLE_SITE_KEY = os.environ.get('GRECAPTCHA_INVISIBLE_SITE_KEY')
GRECAPTCHA_INVISIBLE_SECRET = os.environ.get('GRECAPTCHA_INVISIBLE_SECRET')
GRECAPTCHA_V2_SITE_KEY = os.environ.get('GRECAPTCHA_V2_SITE_KEY')
GRECAPTCHA_V2_SECRET = os.environ.get('GRECAPTCHA_V2_SECRET')

IS_SPLIT_SIZE = int(os.environ.get('IS_SPLIT_SIZE', 200000000))
DEVICE_PROPERTIES_PATH = os.environ.get(
    'DEVICE_PROPERTIES_PATH',
    os.path.join(BASE_DIR, 'tools/libs/gpapi/device.properties'))

PROMOIMAGE_PATH = os.environ.get('PROMOIMAGE_PATH')
TOOLTYPE_PATH = os.environ.get('TOOLTYPE_PATH')
PLATFORM_PATH = os.environ.get('PLATFORM_PATH')
IMAGE_PATH = os.environ.get('IMAGE_PATH')
TOOLS_PATH = os.environ.get('TOOLS_PATH')
VIDEO_PATH = os.environ.get('VIDEO_PATH')
SPLITS_PATH = os.environ.get('SPLITS_PATH')
BLOG_LOGO_PATH = os.environ.get('BLOG_LOGO_PATH')
BLOG_IMAGE_PATH = os.environ.get('BLOG_IMAGE_PATH')
ANDROID_VERSION_CODE_PREFIX_TEMPLATE = os.environ.get(
    'ANDROID_VERSION_CODE_PREFIX_TEMPLATE', '{appname}/{version_code}')
ANDROID_TOOLS_PREFIX_TEMPLATE = os.environ.get('ANDROID_TOOLS_PREFIX_TEMPLATE', '{appname}')
TOOLS_PREFIX = os.environ.get('TOOLS_PREFIX', 'apps')
ANDROID_PREFIX = os.environ.get('ANDROID_PREFIX', 'androidtools')
CONFIG_PREFIX = os.environ.get('CONFIG_PREFIX', 'configuration')
MEDIA_PREFIX = os.environ.get('MEDIA_PREFIX', 'mediafiles')

HELPDESK_ENDPOINT = os.environ.get('HELPDESK_ENDPOINT', None)
HELPDESK_API_TOKEN = os.environ.get('HELPDESK_API_TOKEN', None)
HELPDESK_USERS_GROUP_ID = int(os.environ.get('HELPDESK_USERS_GROUP_ID', 0))

# END PATH CONFIGURATION

SECRET_KEY = os.environ.get('SECRET_KEY')

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ORIGIN_WHITELIST = [FRONT_WEB_URL] if FRONT_WEB_URL is not None else []

CORS_ORIGIN_REGEX_WHITELIST = [
    r"^http:\/\/(10\.)[\d\.]+(:\d+)?$",
    r"^http:\/\/(172\.1[6-9]\.)[\d\.]+(:\d+)?$",
    r"^http:\/\/(172\.2[0-9]\.)[\d\.]+(:\d+)?$",
    r"^http:\/\/(172\.3[0-1]\.)[\d\.]+(:\d+)?$",
    r"^http:\/\/(192\.168\.)[\d\.]+(:\d+)?$",
    r"^http:\/\/localhost(:\d+)?$",
]

# Cookie security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

INSTALLED_APPS = [
    'user_management',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.sitemaps',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_hosts',
    'sslserver',
    'rest_framework',
    'rest_framework.authtoken',
    'markdownx',
    'customfilters',                    # TODO: Do we need this?
    'tools',
    'preferences',
    # 's3_email',
    'paskoocheh',
    'pipeline',
    'stats',
    'statsweb',
    'blog',
    'webfrontend',

    'corsheaders',
    'strawberry.django',
    'strawberry_django',
    'gqlauth',

    'accounts',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.styleguide',
    'wagtail.contrib.sitemaps',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    'wagtail.locales',
    "wagtail.contrib.simple_translation",
    "wagtailmarkdown",

    'modelcluster',
    'taggit',

    'blog_wagtail',
    'static_page',
    'rewards',
]

SITE_ID = 1

MIDDLEWARE = [
    'paskoocheh.middleware.RevisionMiddleware',
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'gqlauth.core.middlewares.django_jwt_middleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'webfrontend.middleware.RequestProcessingAndInterceptionMiddleware',
    'paskoocheh.middleware.ResponseAndViewManipulationMiddleware',
    'webfrontend.middleware.InterceptCsrfErrorMiddleware',
    'webfrontend.middleware.ResponseManipulationMiddleware',
    'paskoocheh.middleware.LocaleMiddleware',            # TODO: What is this?
    'paskoocheh.middleware.AdminLocaleURLMiddleware',    # TODO: What is this?
    'paskoocheh.middleware.ExceptionLoggingMiddleware',  # TODO: What is this?
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.mail.com')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '587')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'alias@mail.com')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'alias@mail.com')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'alias@mail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'yourpassword')

STRAWBERRY_DJANGO = {
    "GENERATE_ENUMS_FROM_CHOICES": True,
    "MAP_AUTO_ID_AS_GLOBAL_ID": True
}

username_field = StrawberryField(
    python_name="username", default=None, type_annotation=StrawberryAnnotation(str)
)
password_field = StrawberryField(
    python_name="password", default=None, type_annotation=StrawberryAnnotation(str)
)
email_field = StrawberryField(
    python_name="email", default=None, type_annotation=StrawberryAnnotation(str)
)

INVITATION_PATH_ON_EMAIL = 'register'
EMAIL_SUBJECT_ACTIVATION = 'email/activation_subject.txt'
EMAIL_SUBJECT_INVITATION = 'email/invitation_subject.txt'
EMAIL_TEMPLATE_INVITATION = 'email/invitation_email.html'

GQL_AUTH = GqlAuthSettings(
    LOGIN_REQUIRE_CAPTCHA=False,
    REGISTER_REQUIRE_CAPTCHA=False,
    LOGIN_FIELDS={username_field},
    ALLOW_LOGIN_NOT_VERIFIED=False,
    ALLOW_PASSWORDLESS_REGISTRATION=False,
    ALLOW_DELETE_ACCOUNT=True,
    SEND_PASSWORD_SET_EMAIL=False,
    EXPIRATION_ACTIVATION_TOKEN=timedelta(days=3),
    EXPIRATION_PASSWORD_RESET_TOKEN=timedelta(minutes=30),
    REGISTER_MUTATION_FIELDS=set([email_field, username_field]),
    # TODO: specify UPDATE_MUTATION_FIELDS
    # UPDATE_MUTATION_FIELDS=set([email_field]),
    EMAIL_FROM=DjangoSetting.override(DEFAULT_FROM_EMAIL),
    SEND_ACTIVATION_EMAIL=True,
    PASSWORD_SET_PATH_ON_EMAIL='password-set',
    PASSWORD_RESET_PATH_ON_EMAIL='fa/reset-password',
    ACTIVATION_PATH_ON_EMAIL='fa/activate',
    EMAIL_SUBJECT_PASSWORD_RESET='email/password_reset_subject.txt',
    EMAIL_TEMPLATE_PASSWORD_RESET='email/password_reset_email.html',
    EMAIL_TEMPLATE_ACTIVATION='email/activation_email.html',
    EMAIL_TEMPLATE_VARIABLES={},
    JWT_LONG_RUNNING_REFRESH_TOKEN=True,
    JWT_EXPIRATION_DELTA=timedelta(days=7),
    JWT_REFRESH_EXPIRATION_DELTA=timedelta(days=7),
)

ROOT_HOSTCONF = 'paskoocheh.hosts'
DEFAULT_HOST = 'apex'

ROOT_URLCONF = 'paskoocheh.urls'
WSGI_APPLICATION = 'paskoocheh.wsgi.application'

# AUTH_USER_MODEL = 'authentication.Account'

# Language configuration
LANGUAGE_COOKIE_NAME = 'LANG'
LANGUAGE_COOKIE_AGE = 60 * 60 * 24 * 7
LANGUAGE_CODE = 'ar' if PLATFORM == 'zanga' else 'fa'
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

LANGUAGES = [
    ('en', _('English')),
    ('fa', _('Farsi')),
    ('ar', _('Arabic'))
]

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES

# Django Fixtures
FIXTURE_DIRS = (
    'fixtures/',
)

# Django Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'webfrontend.context_processors.view_body_class',
            ],
        }
    }
]

if (
    env_settings_module.BUILD_ENV == 'development' and
    env_settings_module.DEBUG
):
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        (
            'django.template.loaders.filesystem.Loader',
            [
                os.path.join(BASE_DIR, 'templates')
            ],
        ),
        'django.template.loaders.app_directories.Loader',
    ]
else:
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        (
            'django.template.loaders.cached.Loader',
            [
                (
                    'django.template.loaders.filesystem.Loader',
                    [
                        os.path.join(BASE_DIR, 'templates')
                    ],
                ),
                'django.template.loaders.app_directories.Loader',
            ],
        ),
    ]

# CKEditor settings
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_JQUERY_URL = '//code.jquery.com/jquery-latest.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'height': 200,
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_Custom': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
                'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                'HiddenField']},
            '/',
            {'name': 'basicstyles',
                'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
                'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
                'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                 'Preview',
                 'Maximize',
            ]},
        ],
        'toolbar': 'Custom'
    },
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'paskoocheh/static')
]

STATICFILES_STORAGE = 'paskoocheh.pipeline_storages.S3PipelineManifestStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Hack to fix Pipeline when running in development server
# Via https://github.com/jazzband/django-pipeline/issues/487#issuecomment-230700897
if IS_DEVELOPMENT_SERVER and BUILD_ENV == 'production':
    STATICFILES_FINDERS = (
        STATICFILES_FINDERS +
        ('paskoocheh.pipeline_finders.DevelopmentPipelineFinder',)
    )
elif BUILD_ENV == 'production':
    STATICFILES_FINDERS = (
        STATICFILES_FINDERS +
        ('pipeline.finders.ManifestFinder',)
    )

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

PIPELINE = {
    'PIPELINE_COLLECTOR_ENABLED': False,

    'MIMETYPES': (
        ('text/javascript', '.js'),
    ),

    'STYLESHEETS': {
        'statsweb_global': {
            'source_filenames': (
                'statsweb/lib/pikaday-1.5.1.css',
                f'statsweb/css/{PLATFORM}-stats.css',
            ),
            'output_filename': 'statsweb/global-bundle.css',
        },
        'webfrontend_global': {
            'source_filenames': (
                'webfrontend/css/star-rating.css',
                'webfrontend/css/star-rating-theme.css',
                'webfrontend/css/android-promo-notice.css',
                'webfrontend/css/blog-associated-tool-list.css',
                'webfrontend/css/blog-associated-tool-list-item.css',
                'webfrontend/css/blog-associated-post-list.css',
                'webfrontend/css/blog-associated-post-list-item.css',
                'webfrontend/css/blogindex.css',
                'webfrontend/css/blogpost.css',
                'webfrontend/css/blogposts.css',
                'webfrontend/css/blog-post-list.css',
                'webfrontend/css/blog-post-list-item.css',
                'webfrontend/css/boxed-standalone.css',
                'webfrontend/css/button.css',
                'webfrontend/css/expandable-list.css',
                'webfrontend/css/form.css',
                'webfrontend/css/form-recaptcha-fallback.css',
                f'webfrontend/css/{PLATFORM}-global.css',
                f'webfrontend/css/{PLATFORM}-html-content.css',
                'webfrontend/css/images-carousel.css',
                'webfrontend/css/index.css',
                'webfrontend/css/index-section.css',
                'webfrontend/css/invisible-grecaptcha.css',
                f'webfrontend/css/{PLATFORM}-main-footer.css',
                f'webfrontend/css/{PLATFORM}-main-header.css',
                f'webfrontend/css/{PLATFORM}-mobile-menu.css',
                'webfrontend/css/overlay.css',
                f'webfrontend/css/{PLATFORM}-page.css',
                'webfrontend/css/review.css',
                'webfrontend/css/review-list.css',
                'webfrontend/css/search.css',
                'webfrontend/css/toolversion.css',
                'webfrontend/css/toolversion-badge.css',
                'webfrontend/css/toolversion-main.css',
                'webfrontend/css/toolversion-main-download-links.css',
                'webfrontend/css/toolversion-main-guides-support.css',
                'webfrontend/css/toolversion-main-reviews.css',
                'webfrontend/css/toolversion-nav.css',
                'webfrontend/css/toolversion-review-overlay.css',
                'webfrontend/css/toolversion-support-overlay.css',
                'webfrontend/css/toolversionguide.css',
                'webfrontend/css/toolversionreview.css',
                'webfrontend/css/toolversionreviews.css',
                'webfrontend/css/toolversiontutorial.css',
                'webfrontend/css/tool-list.css',
                'webfrontend/css/tool-list-item.css',
                'webfrontend/css/tutorial-list.css',
                'webfrontend/css/embedded-video.css',
                'webfrontend/css/video-wrapper.css',
                'webfrontend/lib/flickity-2.0.10.css',
                'webfrontend/css/share-links.css',
            ),
            'output_filename': 'webfrontend/global-bundle.css',
        },
    },
    'JAVASCRIPT': {
        'statsweb_global': {
            'source_filenames': (
                'statsweb/lib/moment-2.19.2.js',
                'statsweb/lib/plotly-1.19.2.min.js',
                'statsweb/lib/pikaday-1.5.1.js',
                'statsweb/js/stats.js',
                'statsweb/js/utils.js',
                'statsweb/js/charts/channel-downloads-per-day.js',
                'statsweb/js/charts/platform-downloads-per-day.js',
                'statsweb/js/charts/tool-downloads-per-day.js',
                'statsweb/js/charts/total-downloads-per-day.js',
                'statsweb/js/main.js',
            ),
            'output_filename': 'statsweb/global-bundle.js',
        },
        'webfrontend_global': {
            'source_filenames': (
                'webfrontend/lib/jquery-3.4.1.min.js',
                'webfrontend/lib/flickity-2.0.10.pkgd.js',
                'webfrontend/js/star-rating.min.js',
                'webfrontend/js/star-rating-theme.js',
                'webfrontend/js/a11y-shortcut.js',
                'webfrontend/js/android-promo-notice.js',
                'webfrontend/js/expandable-list.js',
                'webfrontend/js/external-download-link.js',
                'webfrontend/js/form-validation.js',
                'webfrontend/js/global-focus-change-event-dispatcher.js',
                'webfrontend/js/global-keydown-event-dispatcher.js',
                'webfrontend/js/images-carousel.js',
                'webfrontend/js/invisible-grecaptcha.js',
                'webfrontend/js/main-header.js',
                'webfrontend/js/mobile-menu.js',
                'webfrontend/js/overlay.js',
                'webfrontend/js/overlay-trigger.js',
                'webfrontend/js/app.js',
                'webfrontend/js/video-wrapper.js',
                'webfrontend/js/main.js',
                'webfrontend/js/js-unsupported.js',
                'webfrontend/js/bundled-app-notice.js',
            ),
            'output_filename': 'webfrontend/global-bundle.js',
        },
        'webfrontend_head': {
            'source_filenames': (
                'webfrontend/js/head.js',
            ),
            'output_filename': 'webfrontend/head.js',
        },
    },

    'JS_COMPRESSOR': 'paskoocheh.pipeline_compressors.UglifyJSCompressor',
    'CSS_COMPRESSOR': 'paskoocheh.pipeline_compressors.CleanCSSCompressor',

    'CLEANCSS_BINARY': 'node_modules/clean-css-cli/bin/cleancss',
    'CLEANCSS_ARGUMENTS': '--compatibility=ie8',
    'UGLIFYJS_BINARY': 'node_modules/uglify-js/bin/uglifyjs',
    'UGLIFYJS_ARGUMENTS': '--ie8',
}

# This tells Pipeline to add the `async` attribute to the bundled script tag,
# which will cause some browsers’ preloaders to start downloading it earlier.
# We don’t want `async` to be added to the separated script tags in development
# since async script tags can be executed in any order, which could cause
# problems if main.js ran before anything else.

# Commented out for version 0.9.1 as a potential fix for intermittent layout
# issues, which could be related to the timing of scripts marked as async.
# TODO: Remove if this turns out to work.

# if BUILD_ENV == 'production':
#     PIPELINE['JAVASCRIPT']['webfrontend_global']['extra_context'] = {
#         'async': True,
#     }

ACCEPTABLE_IMAGES = ['gif', 'jpg', 'jpeg', 'png', 'svg']

# S3 metadata for telegram servers
S3_METADATA_FILE_ID = 'file_id'


# CHOICES
# Languages supported
LANGUAGE_SUPPORTED_CHOICES = (
    ('en', 'English'),
    ('fa', 'Persian'),
    ('ar', 'Arabic'))
LANGUAGE_SUPPORTED_DEFAULT = 'fa'

# Various Paskoocheh Interfaces
PASKOOCHEH_CHANNEL_CHOICES = (
    ('BOT', 'Telegram Bot'),
    ('EMAIL', 'Email Auto Responder'),
    ('ANDROID', 'Android App'),
    ('WEB', 'Website')
)

# Reviews
MAX_REVIEWS_TO_STORE_IN_JSON = 1000

# Any code that results in data being stored (analytics, forms, etc.) should
# check the request’s user agent against these regular expressions first.
NOOP_USER_AGENT_PATTERNS = (
    re.compile('sysops'),
)

# Django Rest Framework settings
REST_FRAMEWORK = {
    'PAGE_SIZE': 25,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': [
        'v1',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'paskoocheh',
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1200
# If this is False, session data will only be saved if modified
SESSION_SAVE_EVERY_REQUEST = True

MARKDOWNX_IMAGE_MAX_SIZE = {
    'size': (9999, 9999),
    'quality': 100,
}

MARKDOWNX_UPLOAD_CONTENT_TYPES = [
    'image/gif',
    'image/jpeg',
    'image/png',
]
MARKDOWNX_UPLOAD_BYPASS_IMAGE_PROCESSING_CONTENT_TYPES = (
    'image/gif',
    'image/jpeg',
    'image/png',
)

# Webfrontend-specific settings
WEBFRONTEND_CACHE_RESPONSE_ENABLED = (
    os.environ.get('WEBFRONTEND_CACHE_RESPONSE_ENABLED', None) not in ('0', 'false')
)
WEBFRONTEND_CACHE_RESPONSE_TIMEOUT = (
    int(os.environ['WEBFRONTEND_CACHE_RESPONSE_TIMEOUT'])
    if os.environ.get('WEBFRONTEND_CACHE_RESPONSE_TIMEOUT')
    else 86400  # 24 hours
)

WEBFRONTEND_DEFAULT_IMAGE_PATH = f'/static/webfrontend/images/{PLATFORM}-logo.svg'

WEBFRONTEND_CANONICAL_HOST = os.environ.get('WEBFRONTEND_CANONICAL_HOST')
WEBFRONTEND_CANONICAL_SCHEME = os.environ.get('WEBFRONTEND_CANONICAL_SCHEME')
WEBFRONTEND_ENFORCE_CANONICAL_SCHEME_AND_HOST = (
    os.environ.get('WEBFRONTEND_ENFORCE_CANONICAL_SCHEME_AND_HOST') == 'true'
)
SERVER_DIRECT_URL = os.environ.get('SERVER_DIRECT_URL', WEBFRONTEND_CANONICAL_HOST)

TELEGRAPH_AUTHOR_URL = f'https://{PLATFORM}.{TOP_LEVEL_DOMAIN}/'

# Google Tag Manager settings
GOOGLE_TAG_MANAGER_CONTAINER_ID = os.environ.get('GOOGLE_TAG_MANAGER_CONTAINER_ID', None)

S3_INTERNET_SHUTDOWN_DIR = 'internet-shutdown'

# non installable file extension checklist for config file (configfile.py)
NON_INSTALLABLE_FILE_EXTENSIONS = ['pdf', 'html']

# Wagtail setting to use a custom image model
WAGTAILIMAGES_IMAGE_MODEL = 'static_page.CaptionedImage'

# Don't add a trailing slash to Wagtail-served URLs
WAGTAIL_APPEND_SLASH = False

WAGTAIL_SITE_NAME = 'Site'
WAGTAILADMIN_BASE_URL = FRONT_WEB_URL
WAGTAIL_EMAIL_MANAGEMENT_ENABLED = False
WAGTAIL_I18N_ENABLED = True
WAGTAIL_ALLOW_UNICODE_SLUGS = False  # Suppress unicode page slugs

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    },
}

WAGTAILMARKDOWN = {
    "autodownload_fontawesome": False,
    "allowed_tags": [],  # optional. a list of HTML tags. e.g. ['div', 'p', 'a']
    "allowed_styles": [],  # optional. a list of styles
    "allowed_attributes": {},  # optional. a dict with HTML tag as key and a list of attributes as value
    "allowed_settings_mode": "extend",  # optional. Possible values: "extend" or "override". Defaults to "extend".
    "extensions": [],  # optional. a list of python-markdown supported extensions
    "extension_configs": {},  # optional. a dictionary with the extension name as key, and its configuration as value
    "extensions_settings_mode": "extend",  # optional. Possible values: "extend" or "override". Defaults to "extend".
}
