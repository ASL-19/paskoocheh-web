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

from django.http import HttpResponse
from django.views import View


class SetAndroidPromoNoticeHiddenCookieView(View):
    u"""Handler for PUT /set-platform (doesn’t render)."""

    def put(self, request, *args, **kwargs):
        u"""
        Set global_platform cookie to provided platform slug, redirect to
        /?platform={{global_platform}}

        Returns:
            HttpResponseRedirect (302)
        """
        response = HttpResponse()

        response.set_cookie(
            httponly=True,
            key='android_promo_notice_hidden',
            max_age=604800,
            secure=True,
            value='true'
        )

        return response
