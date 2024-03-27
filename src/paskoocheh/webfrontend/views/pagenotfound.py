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

from django.shortcuts import render
from django.utils.translation import pgettext
from django.views import View
from webfrontend.templatetags.pk_meta_tags import PkViewMetadata


class PageNotFoundView(View):
    u"""View for 404 pages."""

    def get(self, request, *args, **kwargs):
        return self.render_error_view(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        return self.render_error_view(request, args, kwargs)

    def render_error_view(self, request, args, kwargs):
        u"""Generate a 404 page response.

        Args:
            **error_message (string): The error message to display.

        Returns:
            HttpResponse
        """
        # Translators: Default error page message
        error_message = pgettext(
            u'Error message',
            u'Unspecified error.'
        )
        status = 404
        # Translators: Default error page title
        status_string = pgettext(
            u'Error title',
            u'Page not found'
        )

        if 'error_message' in kwargs:
            error_message = kwargs['error_message']

        if 'status' in kwargs:
            status = kwargs['status']

            if status == 400:
                # Translators: Appears if the server can’t deal with a request
                # because it contains bad/invalid data, e.g. if an invalid
                # review is submitted
                status_string = pgettext(
                    u'Error title',
                    u'Bad request'
                )
            elif status == 500:
                # Translators: Appears if the server can’t deal with a request
                # because of an unexpected server issue.
                status_string = pgettext(
                    u'Error title',
                    u'Internal server error'
                )

        if 'status_string' in kwargs:
            status_string = kwargs['status_string']

        if status == 200:
            page_title = status_string
        else:
            page_title = '{status}: {status_string}'.format(
                status=status,
                status_string=status_string
            )

        view_metadata = PkViewMetadata(
            title=page_title,
        )

        return render(
            request,
            'webfrontend/pagenotfound.html',
            status=status,
            context={
                'error_message': error_message,
                'page_title': page_title,
                'status': status,
                'status_string': status_string,
                'view_metadata': view_metadata,
            }
        )
