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

from blog.models import Post
from django.shortcuts import render
from django.utils.translation import pgettext
from django.views import View
from webfrontend.caches.responses.decorators import pk_cache_response
from webfrontend.utils.uri import pask_reverse

FEED_POSTS_COUNT = 20


class BlogPostsFeedView(View):
    u"""Blog posts feed."""

    @pk_cache_response()
    def get(self, request, **kwargs):
        u"""
        Generate blog posts Atom feed.

        Returns:
            HttpResponse
        """

        posts = (
            Post.objects
            .filter(
                language=self.request.LANGUAGE_CODE,
                status='p',
            )
            .order_by('-published_date')
        )[:FEED_POSTS_COUNT]

        feed_updated_datetime = None
        for post in posts:
            if (
                feed_updated_datetime is None or
                post.last_modified_date > feed_updated_datetime
            ):
                feed_updated_datetime = post.last_modified_date

        if feed_updated_datetime:
            feed_updated_datetime_iso8601 = (
                feed_updated_datetime
                .replace(microsecond=0)
                .isoformat()
            )
        else:
            feed_updated_datetime_iso8601 = ''

        blog_posts_url = request.build_absolute_uri(
            pask_reverse(
                'webfrontend:blogposts',
                request,
            )
        )

        blog_posts_feed_url = request.build_absolute_uri(
            pask_reverse(
                'webfrontend:blogpostsfeed',
                request,
            )
        )

        description = pgettext(
            u'Blog',
            u'Description of Paskoocheh blog',
        )

        title = pgettext(
            u'Blog',
            u'Paskoocheh blog',
        )

        return render(
            self.request,
            'webfrontend/blogpostsfeed.xml',
            content_type='application/atom+xml; charset=utf-8',
            context={
                'blog_posts_url': blog_posts_url,
                'blog_posts_feed_url': blog_posts_feed_url,
                'description': description,
                'feed_updated_datetime_iso8601': feed_updated_datetime_iso8601,
                'posts': posts,
                'title': title,
            },
        )
