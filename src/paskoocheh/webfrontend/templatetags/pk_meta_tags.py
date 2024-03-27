# coding: utf-8
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

u"""Registers pk_meta_tags Django template tag."""

import attr
from django import template
from django.templatetags.static import static
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import pgettext, gettext
from markdownx.utils import markdownify
from django.conf import settings
register = template.Library()

app = settings.PLATFORM


@attr.s(frozen=True, slots=True)
class PkViewMetadata(object):
    u"""
    Immutable object containing view metadata.

    Attributes:
        description (unicode): Short description of view, suggested to search
            engines and social media platforms
        description_is_markdown (bool)
        title (unicode): Title of view, not including “ – Paskoocheh/Zanga”, which is
            automatically appended
        image_height (int): Height of images in pixels, if applicable. Only
            used if width also provided.
        image_url (unicode): URL of image to be suggested for social media
            previews
        image_width (int): Width of images in pixels, if applicable. Only used
            if height also provided.
    """
    description = attr.ib(default=None)
    description_is_markdown = attr.ib(default=False)
    image_alt = attr.ib(default=None)
    image_height = attr.ib(default=None)
    image_url = attr.ib(default=None)
    image_width = attr.ib(default=None)
    facebook_is_article = attr.ib(default=False)
    title = attr.ib(default=None)
    twitter_image_is_large = attr.ib(default=False)


@register.inclusion_tag(
    'webfrontend/tags/meta_tags.html',
    takes_context=True,
)
def pk_meta_tags(context, view_metadata):
    u"""
    Build the context for the pk_meta_tags inclusion tag.

    Args:
        view_metadata (PkViewMetadata)

    Returns:
        dictionary: Template context
    """
    app_name_translation = gettext(u'Zanga' if app == 'zanga' else u'Paskoocheh')

    title_with_app_name = app_name_translation
    title_without_app_name = app_name_translation

    if view_metadata.title:
        title_with_app_name = '{title} – {app_name}'.format(
            title=view_metadata.title,
            app_name=app_name_translation,
        )
        title_without_app_name = view_metadata.title

    # If description isn’t provided (is None), a generic description is
    # rendered instead. If description is False, nothing will be rendered.
    description = view_metadata.description

    if view_metadata.description_is_markdown:
        html_description = markdownify(description)
        plain_text_description = strip_tags(html_description)
        description = plain_text_description

    if type(description) in [str]:
        description = (
            Truncator(description)
            .words(30)
            .replace('...', '…')
        )
    elif description is None:
        description = pgettext(
            u'Metadata',
            # Translators: This is the default site description suggested to
            # search engines and social media previews. It’s used if the page
            # doesn’t have its own description (e.g. tool pages will use the
            # tool description). (The English is a placeholder.)
            u'An open-source app store enabling easy access to circumvention and privacy tools.'
        )

    absolute_image_url = None
    if settings.BUILD_ENV == 'local':
        fallback_image_url = context.request.build_absolute_uri(
            static(f'webfrontend/images/{app}-logo-meta-1000w.png')
        )
        fallback_image_facebook_url = context.request.build_absolute_uri(
            static(f'webfrontend/images/{app}-logo-meta-314w.png')
        )

        if view_metadata.image_url:
            absolute_image_url = view_metadata.image_url

    else:
        fallback_image_url = '{canonical_scheme}://{canonical_host}{path}'.format(
            canonical_scheme=settings.WEBFRONTEND_CANONICAL_SCHEME,
            canonical_host=settings.WEBFRONTEND_CANONICAL_HOST,
            path=f'/static/webfrontend/images/{app}-logo-meta-1000w.png'
        )
        fallback_image_facebook_url = '{canonical_scheme}://{canonical_host}{path}'.format(
            canonical_scheme=settings.WEBFRONTEND_CANONICAL_SCHEME,
            canonical_host=settings.WEBFRONTEND_CANONICAL_HOST,
            path=f'/static/webfrontend/images/{app}-logo-meta-314w.png'
        )

    if view_metadata.image_url:
        absolute_image_url = '{canonical_scheme}://{canonical_host}{path}'.format(
            canonical_scheme=settings.WEBFRONTEND_CANONICAL_SCHEME,
            canonical_host=settings.WEBFRONTEND_CANONICAL_HOST,
            path=view_metadata.image_url
        )

    fallback_image_facebook_height = 314
    fallback_image_facebook_width = 314

    return {
        'canonical_url': context.request.canonical_url,
        'description': description,
        'image_alt': view_metadata.image_alt,
        'image_height': view_metadata.image_height,
        'image_url': absolute_image_url,
        'image_width': view_metadata.image_width,
        'facebook_is_article': view_metadata.facebook_is_article,
        'fallback_image_url': fallback_image_url,
        'fallback_image_facebook_url': fallback_image_facebook_url,
        'fallback_image_facebook_height': fallback_image_facebook_height,
        'fallback_image_facebook_width': fallback_image_facebook_width,
        'title_with_app_name': title_with_app_name,
        'title_without_app_name': title_without_app_name,
        'twitter_image_is_large': view_metadata.twitter_image_is_large,
        'app': app,
        'app_name_translation': app_name_translation,
    }
