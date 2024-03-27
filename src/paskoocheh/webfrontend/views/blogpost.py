from blog.models import Post
from dateutil import parser as dateutil_parser
from django.shortcuts import render
from django.utils.translation import pgettext
from django.views import View
from webfrontend.caches.responses.decorators import pk_cache_response
from webfrontend.templatetags.pk_meta_tags import PkViewMetadata
from webfrontend.utils.blog import get_localized_blog_category_name
from webfrontend.utils.general import (
    gregorian_datetime_to_jalali_date_string,
    image_exists,
)
from webfrontend.utils.uri import pask_reverse
from django.conf import settings
from django.db.models import Q

app = settings.PLATFORM


class BlogPostView(View):
    u"""Blog post."""

    @pk_cache_response()
    def get(self, request, **kwargs):
        u"""
        Generate a blog post view response.

        Returns:
            HttpResponse
        """
        from webfrontend.views import PageNotFoundView

        try:
            post_date = dateutil_parser.parse(
                self.kwargs.get('post_date')
            )

            post = (
                Post.objects
                .get(
                    published_date__date=post_date,
                    slug=self.kwargs.get('post_slug'),
                )
            )
        except Post.DoesNotExist:
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        # Translators: This could happen if the URL is wrong or
                        # outdated (e.g. we delete it, change the slug).
                        u'No blog post matching this URL exists.',
                    )
                ),
                status=404
            )

        post_published_datetime_iso8601 = (
            post.published_date
            .replace(microsecond=0)
            .isoformat()
        )
        post_published_date_iso8601 = post_published_datetime_iso8601[:10]
        post_published_date_jalali = gregorian_datetime_to_jalali_date_string(
            post.published_date
        )

        post_category_name = get_localized_blog_category_name(
            post.category,
            request,
        )

        url = self.request.build_absolute_uri(
            pask_reverse(
                'webfrontend:blogpost',
                self.request,
                p_post_date=post_published_date_iso8601,
                p_post_slug=post.slug,
            )
        )

        title = post.title

        view_metadata = {
            'description': post.summary,
            'facebook_is_article': True,
            'title': post.title,
        }

        feature_image = None
        feature_image_inline_style = None

        if image_exists(post.feature_image):
            feature_image = post.feature_image

            height_to_width_percentage = (
                (float(feature_image.height) / float(feature_image.width)) * 100
            )

            feature_image_inline_style = (
                "display: block; content: ' '; padding-bottom: {height_to_width_percentage}%;".format(
                    height_to_width_percentage=height_to_width_percentage
                )
            )

            view_metadata.update({
                'image_width': feature_image.width,
                'image_height': feature_image.height,
                'image_url': feature_image.url,
                'twitter_image_is_large': True,
            })

            if post.feature_image_caption:
                view_metadata.update({
                    'image_alt': post.feature_image_caption,
                })

        associated_tools = post.tool_tag.all()
        associated_versions = post.version_tag.all()

        tags_list = list(post.tags.values_list('slug', flat=True))
        related_posts = (
            Post.objects
            .filter(
                Q(language=self.request.LANGUAGE_CODE) &
                Q(status='p') &
                Q(tags__slug__in=tags_list)
            )
            .exclude(pk=post.pk)
            .order_by('-published_date')
            [:3]
        )

        view_metadata = PkViewMetadata(**view_metadata)

        return render(
            self.request,
            'webfrontend/blogpost.html',
            context={
                'associated_tools': associated_tools,
                'associated_versions': associated_versions,
                'related_posts': related_posts,
                'is_blog_page': True,
                'feature_image': feature_image,
                'feature_image_inline_style': feature_image_inline_style,
                'post': post,
                'post_category_name': post_category_name,
                'post_published_datetime_iso8601': post_published_datetime_iso8601,
                'post_published_date_jalali': post_published_date_jalali,
                'url': url,
                'title': title,
                'view_metadata': view_metadata,
                'app': app,
            }
        )
