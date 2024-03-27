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

import logging
import requests
from django.shortcuts import render
from django.utils.translation import pgettext
from django.views import View
from preferences.models import Text, GeneralPreference
from webfrontend.caches.responses.decorators import pk_cache_response
from webfrontend.templatetags.pk_meta_tags import PkViewMetadata
from django.conf import settings
from django.http import HttpResponse
from webfrontend.utils.general import (
    is_request_user_agent_noop,
    send_contact_notification_email,
)

logger = logging.getLogger(__name__)


class PageView(View):
    u"""View for preferences.Text pages."""

    @pk_cache_response()
    def get(self, request, **kwargs):
        u"""
        Generate a page view response.

        Get the requested field from the preferences.Text for the current
        request’s language.

        Args:
            **fieldname (string): preferences.Text field name

        Returns:
            HttpResponse
        """
        from webfrontend.views import PageNotFoundView

        try:
            current_language_text = Text.objects.get(
                language=self.request.LANGUAGE_CODE,
                publishable=True,
            )
        except Text.DoesNotExist:
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        # Translators: Appears if the admin is missing a Web
                        # Text for the current static page (e.g. about, terms
                        # of service)
                        u'This page isn’t available in the current language.',
                    )
                ),
                status=404
            )

        slug = kwargs.get('slug', None)
        field_name = None
        title = None

        if slug == 'about':
            field_name = 'about'
            title = pgettext(
                u'Page title',
                # Translators: Title of about page
                u'What we do'
            )
        elif slug == 'terms-of-service':
            field_name = 'terms_of_service'
            title = pgettext(
                u'Page title',
                # Translators: Title of terms of service page
                u'Terms of service'
            )
        elif slug == 'privacy-policy':
            field_name = 'privacy_policy'
            title = pgettext(
                u'Page title',
                # Translators: Title of privacy policy page
                u'Privacy policy'
            )

        body_markdown = None
        if slug == 'contact':
            title = pgettext(
                u'Page title',
                # Translators: Title of contact us page
                u'Contact us'
            )
        else:
            try:
                body_markdown = getattr(current_language_text, field_name)
            except AttributeError:
                return PageNotFoundView.as_view()(
                    self.request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            # Translators: Appears if the current language’s Web
                            # Text doesn’t have a field for the requested page.
                            # Will only happen if there’s a mistake in the code.
                            u'This page doesn’t exist.',
                        )
                    ),
                    status=404
                )

        view_metadata = PkViewMetadata(
            title=title,
            description=None if slug == 'contact' else body_markdown,
            description_is_markdown=False if slug == 'contact' else True,
        )

        twitter = None
        facebook = None
        instagram = None
        telegram = None

        if GeneralPreference.objects.first():
            obj = GeneralPreference.objects.first()
            twitter = getattr(obj, 'twitter', None)
            facebook = getattr(obj, 'facebook', None)
            instagram = getattr(obj, 'instagram', None)
            telegram = getattr(obj, 'telegram', None)

        app = settings.PLATFORM

        has_social_media_sharelinks = slug == 'about' or slug == 'contact'

        has_banner = has_social_media_sharelinks

        display_contact_success = (
            'contactsuccess' in self.kwargs and
            self.kwargs['contactsuccess'] is True
        )

        return render(
            self.request,
            'webfrontend/page.html',
            context={
                'body_markdown': body_markdown,
                'slug': slug,
                'title': title,
                'view_metadata': view_metadata,
                'twitter': twitter,
                'facebook': facebook,
                'instagram': instagram,
                'telegram': telegram,
                'app': app,
                'current_language_text': current_language_text,
                'has_social_media_sharelinks': has_social_media_sharelinks,
                'has_banner': has_banner,
                'display_contact_success': display_contact_success,
            }
        )

    def post(self, request, **kwargs):
        u"""
        Processes a POST request from the contact us page form and passes
        the arguments to stats.utils.send_contact_notification_email.

        Sets kwargs['contactsuccess'] and returns response from
        PageView.get if successful; returns a PageNotFoundView if
        unsuccessful.

        Returns:
            HttpResponse
        """

        if is_request_user_agent_noop(self.request):
            return HttpResponse(status=403)

        from webfrontend.views import PageNotFoundView

        # =========================
        # === Get email address ===
        # =========================
        user_email = None

        if (
            'email' in self.request.POST
        ):
            user_email = self.request.POST['email']
        if (
            user_email is None or
            user_email == ''
        ):
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'Contact request rejected because email address was blank.',
                    )
                ),
                status=400,
            )

        # ===================
        # === Get country ===
        # ===================
        country = None

        if (
            'country' in self.request.POST
        ):
            country = self.request.POST['country']

        # ===================
        # === Get message ===
        # ===================
        message = None

        if (
            'message' in self.request.POST
        ):
            message = self.request.POST['message']
        if (
            message is None or
            message == ''
        ):
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'Contact request rejected because message was blank.',
                    )
                ),
                status=400,
            )

        # ========================
        # === Verify reCAPTCHA ===
        # ========================
        grecaptcha_valid = self.verify_request_grecaptcha()

        if not grecaptcha_valid:
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'Support request rejected because verification code (reCAPTCHA) was missing or invalid. Please navigate back and try again. If this doesn’t seem right, please contact us.',
                    )
                ),
                status=400,
            )

        # ===============================================
        # === Send notification email to support team ===
        # ===============================================
        send_contact_notification_email(user_email, message, country)

        # =========================================
        # === Delegate response to `get` method ===
        # =========================================
        self.kwargs['contactsuccess'] = True

        return self.get(self.request, slug='contact')

    def verify_request_grecaptcha(self):
        u"""
        Send the POST `g-recaptcha-response` argument to Google for
        verification, return the validity.

        Returns:
            reCAPTCHA validity (bool)
        """
        if 'g-recaptcha-response' not in self.request.POST:
            logger.error(
                u'Couldn’t verify reCAPTCHA because request was missing required g-recaptcha-response POST argument.'
            )
            return False

        if 'grecaptcha-type' not in self.request.POST:
            logger.error(
                u'Couldn’t verify reCAPTCHA because request was missing required grecaptcha-type POST argument.'
            )
            return False

        recaptcha_response = self.request.POST['g-recaptcha-response']
        grecaptcha_secret = None

        if self.request.POST['grecaptcha-type'] == 'invisible':
            grecaptcha_secret = settings.GRECAPTCHA_INVISIBLE_SECRET
        elif self.request.POST['grecaptcha-type'] == 'v2':
            grecaptcha_secret = settings.GRECAPTCHA_V2_SECRET

        if not grecaptcha_secret:
            logger.error(
                u'Couldn’t verify reCAPTCHA because corresponding secret key couldn’t be determined.'
            )
            return False

        verification_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', {
                'secret': grecaptcha_secret,
                'response': recaptcha_response
            }
        )
        verification_response_json = verification_response.json()

        if (
            'success' in verification_response_json and
            verification_response_json['success'] is True
        ):
            return True

        return False
