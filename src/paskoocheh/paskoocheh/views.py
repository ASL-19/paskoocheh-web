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


from urllib import unquote
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.utils import translation

app = settings.PLATFORM


class IndexView(TemplateView):
    """
    Index view definition class
    """

    def __init__(self):
        """
        Init method
        """

        super(IndexView, self).__init__()

    template_name = 'index.html'

    def get_frontend_lang(self):
        """
        Get currently selected language
        """

        front_cookie_value = self.request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        if front_cookie_value:
            return front_cookie_value
        else:
            return None

    def render_to_response(self, context, **response_kwargs):
        """
        Set language cookie
        """

        context['BUILD_ENV'] = settings.BUILD_ENV
        response = super(IndexView, self).render_to_response(context, **response_kwargs)
        frontend_lang = self.get_frontend_lang()
        if frontend_lang:
            # translation activate doesn't accept quoted cookie values
            translation.activate(unquote(frontend_lang).strip('\''))
        else:
            translation.activate(settings.LANGUAGE_CODE)
            # The cookie value should be encoded, %22 represents double quotation,
            # javascript only accept double quote
            # while python works with no quote
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, '%22ar%22' if app == 'zanga' else '%22fa%22',
                                max_age=settings.LANGUAGE_COOKIE_AGE)
        return response

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        """
        Dispatch method
        """

        return super(IndexView, self).dispatch(*args, **kwargs)
