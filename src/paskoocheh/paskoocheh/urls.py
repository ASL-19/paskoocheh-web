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

from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.views.static import serve
from django.conf.urls.i18n import i18n_patterns
from tools.views import delete_file_id, report_devices

from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView
from paskoocheh.schema import schema

from paskoocheh.sitemaps import (
    AboutPageSitemapEntry,
    TermsPageSitemapEntry,
    PolicyPageSitemapEntry,
    ContactPageSitemapEntry,
    VersionSitemap,
    PostSitemap,
    FaqSitemap,
    GuideSitemap,
    TutorialSitemap,
)
from django.contrib.sitemaps.views import sitemap

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.documents.models import Document
from wagtail import urls as wagtail_urls
from taggit.models import Tag


sitemaps = {
    'about': AboutPageSitemapEntry,
    'terms': TermsPageSitemapEntry,
    'policy': PolicyPageSitemapEntry,
    'contact': ContactPageSitemapEntry,
    'versions': VersionSitemap,
    'posts': PostSitemap,
    'faqs': FaqSitemap,
    'guides': GuideSitemap,
    'tutorials': TutorialSitemap,
}

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'^sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('markdownx/', include('markdownx.urls')),
    re_path(r'^api/(?P<version>(v1))/deletefileid/(?P<version_id>[0-9]+)/$', delete_file_id, name='deletefileid'),
    re_path(r'^api/(?P<version>(v1))/reportdevices/', report_devices, name='reportdevices'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/webfrontend/favicons/favicon.ico', permanent=True)),
    re_path(r'^graphql/', csrf_exempt(GraphQLView.as_view(schema=schema, graphiql=settings.DEBUG))),
]

urlpatterns += [
    path('', include('webfrontend.urls'), {'path_prefix': ''}),
]

urlpatterns += i18n_patterns(
    path('', include(wagtail_urls)),
)

admin.site.unregister(Tag)
admin.site.unregister(Document)
