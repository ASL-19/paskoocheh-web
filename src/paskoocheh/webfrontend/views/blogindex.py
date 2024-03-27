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
from blog.models import Post, Category
from webfrontend.caches.responses.decorators import pk_cache_response
from webfrontend.templatetags.pk_meta_tags import PkViewMetadata
from webfrontend.utils.blog import get_blog_post_list_title
from django.db.models import Count


class BlogIndexView(View):
    u"""Blog index."""

    @pk_cache_response()
    def get(self, request, **kwargs):
        u"""
        Generate a blog index view response.

        Returns:
            HttpResponse
        """
        latest_posts = (
            Post.objects
            .filter(
                language=self.request.LANGUAGE_CODE,
                status='p',
            )
            .order_by('-published_date')
        )[:6]

        latest_posts_title = get_blog_post_list_title()

        featured_posts = (
            Post.objects
            .filter(
                language=self.request.LANGUAGE_CODE,
                status='p',
                homepage_feature__isnull=False,
            )
            .order_by('homepage_feature')
        )[:3]

        featured_posts_title = get_blog_post_list_title(is_featured=True)

        page_title = pgettext(
            u'Blog',
            # Translators: Title of the Paskoocheh blog. Appears on the blog
            # homepage and in page titles.
            u'Paskoocheh blog',
        )

        page_description = pgettext(
            u'Blog',
            # Translators: Description of the Paskoocheh blog. Provided text is
            # a placeholder! Should be short description of what the blog will
            # contain, suitable for search engine snippets and social media
            # previews.
            u'Description of Paskoocheh blog',
        )

        view_metadata = PkViewMetadata(
            description=page_description,
            title=page_title,
        )

        categories = Category.objects.annotate(num_post=Count('post')).filter(num_post__gt=0)

        return render(
            self.request,
            'webfrontend/blogindex.html',
            context={
                'featured_posts': featured_posts,
                'featured_posts_title': featured_posts_title,
                'is_blog_page': True,
                'latest_posts': latest_posts,
                'latest_posts_title': latest_posts_title,
                'page_title': page_title,
                'view_metadata': view_metadata,
                'categories': categories
            }
        )
