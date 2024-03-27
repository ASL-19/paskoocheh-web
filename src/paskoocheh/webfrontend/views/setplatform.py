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

from django.shortcuts import redirect
from django.utils.translation import pgettext
from django.views import View
from webfrontend.utils.uri import pask_reverse
from webfrontend.views import PageNotFoundView


class SetPlatformView(View):
    u"""Handler for POST /set-platform (doesn’t render)."""

    def post(self, request, *args, **kwargs):
        u"""
        Set global_platform cookie to provided platform slug, redirect to
        /?platform={{global_platform}}

        Returns:
            HttpResponseRedirect (302)
        """

        if 'platform' in request.POST:
            platform_slug = request.POST['platform']
        else:
            return PageNotFoundView.as_view()(
                request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'Required platform parameter missing.',
                    )
                ),
                status=400,
            )

        redirect_url = (
            pask_reverse(
                'webfrontend:index',
                request,
                q_platform=platform_slug
            )
        )

        response = redirect(redirect_url)
        # Note: If changed, be sure to replicate in webfrontend.middleware
        response.set_cookie(
            httponly=True,
            key='global_platform',
            max_age=31536000,
            secure=True,
            value=platform_slug
        )

        return response
