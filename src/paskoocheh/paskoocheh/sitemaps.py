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
from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from tools.models import Version, Faq, Guide, Tutorial
from blog.models import Post
from preferences.models import Text


class VersionSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'monthly'
    priority = 1.0

    def items(self):
        """
            A method to retrieve all publishable Version objects
            whose tool is also publishable and exclude the ones
            with linux32/windows32 platforms as they are not exposed
            to users

            Returns:
            A querySet of Version objects
        """

        return Version.objects.filter(
            tool__publishable=True,
            publishable=True
        ).exclude(
            supported_os__slug_name__in=['linux32', 'windows32']
        ).order_by('id')

    def lastmod(self, obj):
        return obj.last_modified


class PostSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'never'
    priority = 0.5

    def items(self):
        """
            A method to retrieve all publishable Post objects

            Returns:
            A querySet of Post objects
        """

        return Post.objects.filter(status='p').order_by('id')

    def lastmod(self, obj):
        return obj.published_date


class FaqSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        """
            A method to retrieve all publishable Faq
            objects whose tool/version is also publishable
            and exclude the ones with linux32/windows32 versions
            as those versions are not exposed to users

            Returns:
            A querySet of Faq objects
        """

        return Faq.objects.filter(
            tool__publishable=True,
            version__publishable=True,
            publishable=True
        ).exclude(
            version__supported_os__slug_name__in=['linux32', 'windows32']
        ).order_by('id')

    def lastmod(self, obj):
        return obj.last_modified


class GuideSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        """
            A method to retrieve all publishable Guide
            objects whose tool/version is also publishable
            and exclude the ones with linux32/windows32 versions
            as those versions are not exposed to users

            Returns:
            A querySet of Guide objects
        """

        return Guide.objects.filter(
            version__tool__publishable=True,
            version__publishable=True,
            publishable=True
        ).exclude(
            version__supported_os__slug_name__in=['linux32', 'windows32']
        ).order_by('id')

    def lastmod(self, obj):
        return obj.last_modified


class TutorialSitemap(Sitemap):
    protocol = 'https'
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        """
            A method to retrieve all publishable Tutorial
            objects whose tool/version is also publishable
            and exclude the ones with linux32/windows32
            versions as those versions are not exposed to users

            Returns:
            A querySet of Tutorial objects
        """

        return Tutorial.objects.filter(
            version__tool__publishable=True,
            version__publishable=True,
            publishable=True
        ).exclude(
            version__supported_os__slug_name__in=['linux32', 'windows32']
        ).order_by('id')

    def lastmod(self, obj):
        return obj.last_modified


class PageSitemapEntry(Sitemap):
    protocol = 'https'
    changefreq = 'yearly'
    priority = 0.5
    page_slug = None

    def items(self):
        """
            A method to retrieve all publishable Text objects with
            the language code of the running app

            Returns:
            A querySet of Page objects
        """

        return Text.objects.filter(
            publishable=True,
            language=settings.LANGUAGE_CODE
        ).order_by('id')

    def location(self, item):
        # Determine page_slug
        if self.page_slug is not None:
            page_slug = self.page_slug
        if page_slug is None:
            page_slug = 'about'

        return reverse(
            'webfrontend:page',
            args=[page_slug]
        )


class AboutPageSitemapEntry(PageSitemapEntry):
    page_slug = 'about'


class TermsPageSitemapEntry(PageSitemapEntry):
    page_slug = 'terms-of-service'


class PolicyPageSitemapEntry(PageSitemapEntry):
    page_slug = 'privacy-policy'


class ContactPageSitemapEntry(PageSitemapEntry):
    page_slug = 'contact'
