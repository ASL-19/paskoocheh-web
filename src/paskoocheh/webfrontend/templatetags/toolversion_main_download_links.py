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

u"""Registers toolversion_main_download_links Django template tag."""

from django import template
from django.utils.translation import pgettext
from webfrontend.utils.general import enforce_required_args
from django.conf import settings

register = template.Library()

app = settings.PLATFORM


@register.inclusion_tag('webfrontend/tags/toolversion_main_download_links.html')
def toolversion_main_download_links(
    version=None,
    linux32_version=None,
    windows32_version=None,
    version_name_localized=None,
):
    u"""
    Build the context for the toolversion_main_download_links inclusion tag.

    Required args:
        version (Version)
        linux32_version (Version)
        windows32_version (Version)
        version_name_localized (unicode)

    Returns:
        dict: Template context
    """
    enforce_required_args(locals(), 'version', 'version_name_localized')

    version_variant_name_localized = None

    if version.supported_os.slug_name == 'linux' or version.supported_os.slug_name == 'windows':
        version_variant_name_localized = pgettext(
            u'Tool version download links heading',
            # Translators: This is used in the headings above version download
            # links to differentiate between 32-bit and 64-bit versions. The
            # “Linux” and "Windows" platforms you see on the site are actually 64-bit OSes,
            # while 32-bit Linux and Windows are hidden from platform selection. On (64-bit)
            # Linux and Windows version pages, if the tool also has a 32-bit version,
            # 32-bit download links appear beneath the 64-bit download links.
            # For almost all users, 64-bit is the appropriate choice. We could
            # add an explanation to the site if you want.
            u'64-bit',
        )
    elif version.supported_os.slug_name == 'linux32' or version.supported_os.slug_name == 'windows32':
        version_variant_name_localized = pgettext(
            u'Tool version download links heading',
            # Translators: This is used in the headings above version download
            # links to differentiate between 32-bit and 64-bit versions. The
            # “Linux” and "Windows" platforms you see on the site are actually 64-bit OSes,
            # while 32-bit Linux and Windows are hidden from platform selection. On (64-bit)
            # Linux and Windows version pages, if the tool also has a 32-bit version,
            # 32-bit download links appear beneath the 64-bit download links.
            # For almost all users, 64-bit is the appropriate choice. We could
            # add an explanation to the site if you want.
            u'32-bit',
        )

    download_link_custom_badge = None

    if 'apple.com' in version.download_url:
        download_link_custom_badge = {
            'alt': pgettext(
                u'Tool version download link',
                u'Download from Apple App Store',
            ),
            'code': u'app-store',
            'image': u'webfrontend/images/download-link-badges/app-store-ar.svg' if app == 'zanga' else u'webfrontend/images/download-link-badges/app-store.svg',
            'image_aspect_ratio': float(119.66407) / float(40),
        }
    elif u'chrome.google.com' in version.download_url:
        download_link_custom_badge = {
            'alt': pgettext(
                u'Tool version download link',
                u'Download from Google Chrome Web Store',
            ),
            'code': u'chrome-web-store',
            'image': u'webfrontend/images/download-link-badges/chrome-web-store.png',
            'image_aspect_ratio': float(493) / float(146),
        }
    elif u'play.google.com' in version.download_url:
        download_link_custom_badge = {
            'alt': pgettext(
                u'Tool version download link',
                u'Download from Google Play',
            ),
            'code': u'google-play',
            'image': u'webfrontend/images/download-link-badges/google-play-ar.png' if app == 'zanga' else u'webfrontend/images/download-link-badges/google-play-fa.png',
            'image_aspect_ratio': float(564) / float(168),
        }
    elif u'microsoft.com' in version.download_url:
        download_link_custom_badge = {
            'alt': pgettext(
                u'Tool version download link',
                u'Download from Microsoft Store',
            ),
            'code': u'microsoft-store',
            'image': u'webfrontend/images/download-link-badges/microsoft-store.png',
            'image_aspect_ratio': float(856) / float(304),
        }

    paskoocheh_download_link_custom_badge = None

    if version.is_bundled_app:
        paskoocheh_download_link_custom_badge = {
            'alt': pgettext(
                u'Tool version download link',
                u'Get it on Paskoocheh',
            ),
            'code': u'paskoocheh',
            'image': u'webfrontend/images/download-link-badges/paskoocheh-fa.png',
            'image_aspect_ratio': float(218) / float(84),
        }

    return {
        'download_link_custom_badge': download_link_custom_badge,
        'paskoocheh_download_link_custom_badge': paskoocheh_download_link_custom_badge,
        'version': version,
        'linux32_version': linux32_version,
        'windows32_version': windows32_version,
        'version_name_localized': version_name_localized,
        'version_variant_name_localized': version_variant_name_localized,
        'app': app
    }
