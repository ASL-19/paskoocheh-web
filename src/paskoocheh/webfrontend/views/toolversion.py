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
import re
import requests
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import pgettext
from django.views import View
from paskoocheh.helpers import get_client_ip
from stats.utils import (
    save_feedback,
    save_rating,
)
from tools.models import Image, Tool, Version
from webfrontend import __version__ as webfrontend_version
from webfrontend.caches.responses.decorators import pk_cache_response
from webfrontend.mixins import ToolVersionMixin
from webfrontend.templatetags.pk_meta_tags import PkViewMetadata
from webfrontend.utils.general import (
    is_request_user_agent_noop,
    send_support_notification_email,
)

logger = logging.getLogger(__name__)


class ToolVersionView(View, ToolVersionMixin):
    u"""View for tool version page."""

    @pk_cache_response()
    def get(self, request, **kwargs):
        u"""
        Generate a tool version page response.

        Get the tool version matching the named group arguments, render the
        tool version page.

        Args:
            **platform_slug (string): tools.models.Version.slug
            **tool_id (string): tools.models.Tool.id

        Returns:
            HttpResponse
        """
        data_or_error_response = self.get_tool_version_data_or_error_response(
            include_tool_versions=True
        )

        if isinstance(data_or_error_response, HttpResponse):
            return data_or_error_response
        else:
            version_data = data_or_error_response

        # ================================
        # === Get logo and screenshots ===
        # ================================
        # Get logo and screenshots via a single complex query, then split up
        # results via loop. This is necessary because the logo is associated with
        # the tool, while the screenshots are associated with the tool version.

        content_types = ContentType.objects.get_for_models(Tool, Version)

        version_images = (
            Image.objects
            .filter(
                Q(publish=True) &
                (
                    Q(language__isnull=True) |
                    Q(language=self.request.LANGUAGE_CODE)
                ) &
                (
                    (
                        Q(content_type=content_types[Version]) &
                        Q(object_id=version_data.tool_version.id) &
                        Q(image_type='screenshot')
                    ) | (
                        Q(content_type=content_types[Tool]) &
                        Q(object_id=version_data.tool.id) &
                        Q(image_type='logo')
                    )
                )
            )
            .order_by('order')
        )

        tool_screenshots = []
        tool_logo = None

        for image in version_images:
            if not tool_logo and image.image_type == 'logo':
                tool_logo = image
            if image.image_type == 'screenshot':
                tool_screenshots.append(image)

        # =================
        # === Get video ===
        # =================

        tool_video = None
        if version_data.tool_version.video:
            tool_video = version_data.tool_version.video

        display_review_success = (
            'reviewsuccess' in self.kwargs and
            self.kwargs['reviewsuccess'] is True
        )

        display_support_success = (
            'supportsuccess' in self.kwargs and
            self.kwargs['supportsuccess'] is True
        )

        meta_description = False
        if version_data.tool_info and hasattr(version_data.tool_info, 'description'):
            meta_description = version_data.tool_info.description

        meta_image = None
        meta_image_width = None
        meta_image_height = None
        if (
            tool_logo and
            hasattr(tool_logo, 'image') and
            hasattr(tool_logo.image, 'url') and
            re.match(
                r'(.*\.png|.*\.jpg|.*\.jpeg)',
                tool_logo.image.url
            )
        ):
            meta_image = self.request.build_absolute_uri(tool_logo.image.url)
            meta_image_width = tool_logo.image.width
            meta_image_height = tool_logo.image.height

        view_metadata = PkViewMetadata(
            description=meta_description,
            description_is_markdown=bool(meta_description),
            image_height=meta_image_height,
            image_url=meta_image,
            image_width=meta_image_width,
            title=version_data.version_name_localized,
        )

        return render(
            self.request,
            'webfrontend/toolversion.html',
            context={
                'display_review_success': display_review_success,
                'display_support_success': display_support_success,
                'tool': version_data.tool,
                'tool_logo': tool_logo,
                'tool_info': version_data.tool_info,
                'tool_name_localized': version_data.tool_name_localized,
                'tool_screenshots': tool_screenshots,
                'tool_video': tool_video,
                'tool_version': version_data.tool_version,
                'version_name_localized': version_data.version_name_localized,
                'tool_versions': version_data.tool_versions,
                'view_metadata': view_metadata,
            }
        )

    def post(self, request, **kwargs):
        u"""
        Get the requested Version object then delegate the request to
        post_review or post_support based on the POST `type` argument.

        Returns:
            HttpResponse
        """
        if is_request_user_agent_noop(self.request):
            return HttpResponse(status=403)

        from webfrontend.views import PageNotFoundView

        platform_slug_name = self.kwargs['platform_slug']
        tool_id = self.kwargs['tool_id']

        tool_version = (
            Version.objects
            .filter(
                tool_id=tool_id,
                supported_os__slug_name=platform_slug_name,
            )
            .first()
        )

        if tool_version is None:
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'No tool matching this URL exists. The tool may no longer be listed.',
                    )
                ),
            )

        if 'type' in self.request.POST:
            if self.request.POST['type'] == 'review':
                return self.post_review(tool_version)
            if self.request.POST['type'] == 'support':
                return self.post_support(tool_version)

        return PageNotFoundView.as_view()(
            self.request,
            error_message=(
                pgettext(
                    u'Error message',
                    u'The server was unable to identify the form’s data type.',
                )
            ),
            status=400,
        )

    def post_review(self, tool_version):  # noqa: C901
        u"""
        Processes a POST request from a tool version review form and saves a
        new Review. Sets kwargs['reviewsuccess'] and returns response from
        ToolVersionView.get if successful; returns a PageNotFoundView if
        unsuccessful.

        Returns:
            HttpResponse
        """
        from webfrontend.views import PageNotFoundView

        # =======================
        # === Get review text ===
        # =======================
        review_text = None

        if (
            'text' in self.request.POST and
            self.request.POST['text'] is not None and
            self.request.POST['text'] != ''
        ):
            review_text = self.request.POST['text']

        # =========================
        # === Get review rating ===
        # =========================
        review_rating = None

        if (
            'rating' in self.request.POST
        ):
            if self.request.POST['rating'] == '':
                return PageNotFoundView.as_view()(
                    self.request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            u'Review rejected because rating wasn’t specified. Please navigate back and try again.',
                        )
                    ),
                    status=400,
                )

            try:
                review_rating = float(self.request.POST['rating'])
            except ValueError:
                pass

        if (
            review_rating is None or
            review_rating < 0 or
            review_rating > 5 or
            (
                review_rating != 0 and
                review_rating % 0.5 != 0
            )
        ):
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'Review rejected because rating was unspecified or invalid. Please navigate back and try again. If this doesn’t seem right, please contact us.',
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
                        u'Review rejected because verification code (reCAPTCHA) was missing or invalid. Please navigate back and try again. If this doesn’t seem right, please contact us.',
                    )
                ),
                status=400,
            )

        # ===================
        # === Save review ===
        # ===================
        request_ip = get_client_ip(self.request)

        try:
            save_rating(
                version_id=tool_version.id,
                rating=review_rating,
                title=None,
                text=review_text,
                user_id=None,
                channel_version=webfrontend_version,
                request_ip=(request_ip).encode('utf-8'),
                language=settings.LANGUAGE_CODE
            )
        except Version.DoesNotExist:
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'Review rejected because referenced tool version doesn’t exist. If this doesn’t seem right, please contact us.',
                    )
                ),
                status=400,
            )

        # =========================================
        # === Delegate response to `get` method ===
        # =========================================
        self.kwargs['reviewsuccess'] = True

        return self.get(self.request)

    def post_support(self, tool_version):  # noqa: C901
        u"""
        Processes a POST request from a tool version support form and passes
        the arguments to stats.utils.save_feedback.

        Sets kwargs['supportsuccess'] and returns response from
        ToolVersionView.get if successful; returns a PageNotFoundView if
        unsuccessful.

        Returns:
            HttpResponse
        """
        from webfrontend.views import PageNotFoundView

        # =========================
        # === Get email address ===
        # =========================
        support_email = None

        if (
            'email' in self.request.POST
        ):
            support_email = self.request.POST['email']
        if (
            support_email is None or
            support_email == ''
        ):
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'Support request rejected because email address was blank.',
                    )
                ),
                status=400,
            )

        # ===================
        # === Get subject ===
        # ===================
        support_subject = None

        if (
            'subject' in self.request.POST
        ):
            support_subject = self.request.POST['subject']
        if (
            support_subject is None or
            support_subject == ''
        ):
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'Support request rejected because subject was blank.',
                    )
                ),
                status=400,
            )

        # ===================
        # === Get message ===
        # ===================
        support_message = None

        if (
            'message' in self.request.POST
        ):
            support_message = self.request.POST['message']
        if (
            support_message is None or
            support_message == ''
        ):
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'Support request rejected because message was blank.',
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

        # =====================
        # === Save feedback ===
        # =====================
        request_ip = get_client_ip(self.request)

        save_feedback(
            title=support_subject,
            text=support_message,
            user_id=support_email,
            channel_version=webfrontend_version,
            request_ip=(request_ip).encode('utf-8'),
        )

        # ===============================================
        # === Send notification email to support team ===
        # ===============================================
        send_support_notification_email(tool_version, support_email, support_message)

        # =========================================
        # === Delegate response to `get` method ===
        # =========================================
        self.kwargs['supportsuccess'] = True

        return self.get(self.request)

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
