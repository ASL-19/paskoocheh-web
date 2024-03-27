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
import logging
from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.utils.cache import patch_cache_control

logger = logging.getLogger(__name__)


class ExceptionLoggingMiddleware(MiddlewareMixin):
    """
    Middleware for handling/logging exceptions
    """
    def process_exception(self, request, exception):
        logger.exception(u'Error handling request: ' + request.path)


class AdminLocaleURLMiddleware(object):
    """
    Middleware for Admin site
    """
    def __init__(self, get_response):
        """
        Init method
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Set language as english if on admin site
        """
        if request.path.startswith('/admin'):
            translation.activate('en')
            request.LANGUAGE_CODE = 'en'

        return self.get_response(request)


class LocaleMiddleware(object):
    """
    Middleware to set language preference
    """
    def __init__(self, get_response):
        """
        Init method
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process request middleware function
        """
        if settings.PLATFORM == 'zanga':
            translation.activate('ar')
            request.LANGUAGE_CODE = 'ar'
        else:
            translation.activate('fa')
            request.LANGUAGE_CODE = 'fa'

        return self.get_response(request)


class RevisionMiddleware:
    """
    Added code version to the response
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        revision = '{}b{}-{}'.format(
            str(settings.VERSION_NUM),
            str(settings.BUILD_NUM),
            str(settings.GIT_SHORT_SHA))
        response['X-Source-Revision'] = revision

        return response


class ResponseAndViewManipulationMiddleware:
    """
    Middleware that runs before Django calls view.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.s3_url = None

        if hasattr(settings, 'AWS_S3_CUSTOM_DOMAIN'):
            self.s3_url = 'https://{s3_domain}'.format(
                s3_domain=settings.AWS_S3_CUSTOM_DOMAIN
            ).encode()

    def __call__(self, request):

        response = self.get_response(request)
        if (response.status_code < 500):
            if (hasattr(request, 'resolver_match') and
                    hasattr(request.resolver_match, 'namespaces') and
                    isinstance(request.resolver_match.namespaces, list) and
                    'api' in request.resolver_match.namespaces):
                patch_cache_control(
                    response,
                    max_age=0,
                    s_maxage=315360000,
                    public=True,
                )

            if (os.environ.get('BUILD_ENV', None) != 'local' and
                    hasattr(settings, 'AWS_CLOUDFRONT_DISTRIBUTION_ID') and
                    isinstance(settings.AWS_CLOUDFRONT_DISTRIBUTION_ID, str) and
                    len(settings.AWS_CLOUDFRONT_DISTRIBUTION_ID) > 0 and
                    self.s3_url):
                response.content = response.content.replace(
                    self.s3_url,
                    b''
                )

        return response
