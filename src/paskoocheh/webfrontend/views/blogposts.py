import re
from blog.models import Category, Post
from copy import deepcopy
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.translation import pgettext
from django.views import View
from tools.models import Tool, Version
from webfrontend.caches.responses.decorators import pk_cache_response
from webfrontend.templatetags.pk_meta_tags import PkViewMetadata
from webfrontend.utils.blog import (
    get_blog_post_list_title,
    get_localized_blog_category_name,
)
from webfrontend.utils.uri import pask_reverse
from django.db.models import Count
from django.conf import settings

POSTS_PER_PAGE = 10
VERSION_QUERY_STRING_ARG_PATTERN = re.compile(r'^(?P<tool_id>\d+)-(?P<platform_slug>\w+)$')
app = settings.PLATFORM


class BlogPostsView(View):      # noqa C901
    u"""Blog posts index."""

    @pk_cache_response()
    def get(self, request, **kwargs):       # noqa: C901
        u"""
        Generate a blog posts index view response.

        Note: If both tool and version query string arguments are provided,
        posts associated with the version and/or tool (but not necessarily both)
        will be queried.

        Query string args:
            Optional:
                category: Category.slug
                featured: true/false
                    If set to true, filters posts with homepage_feature != None
                tool: Tool.id
                version: {Tool.id}-{Version.slug}
                    Parsed with VERSION_QUERY_STRING_ARG_PATTERN

        Returns:
            HttpResponse
        """
        from webfrontend.views import PageNotFoundView

        # =========================
        # === Parse filter args ===
        # =========================
        order_by = '-published_date'
        pagination_link_reverse_kwargs = {}

        category = None
        is_featured = False
        tool = None
        version = None

        # --- Category ---
        category_arg = self.request.GET.get('category')
        if category_arg:
            try:
                category = (
                    Category.objects
                    .get(
                        slug=category_arg
                    )
                )
            except Category.DoesNotExist:
                return PageNotFoundView.as_view()(
                    self.request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            u'URL contains unknown category code “{category_code}“.',
                        )
                        .format(
                            category_code=category_arg,
                        )
                    ),
                )

            pagination_link_reverse_kwargs['q_category'] = category.slug

        # --- Featured ---
        featured_arg = self.request.GET.get('featured')
        if featured_arg == 'true':
            is_featured = True
            order_by = 'homepage_feature'
            pagination_link_reverse_kwargs['q_featured'] = 'true'
        elif featured_arg is not None:
            return PageNotFoundView.as_view()(
                request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'URL contains invalid featured value.',
                    )
                ),
                status=400,
            )

        # --- Tool ---
        tool_arg = self.request.GET.get('tool')
        if tool_arg:
            try:
                tool_id = int(tool_arg)
            except ValueError:
                return PageNotFoundView.as_view()(
                    request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            u'URL contains invalid tool value.',
                        )
                    ),
                    status=400,
                )

            try:
                tool = (
                    Tool.objects
                    .get(
                        id=tool_id
                    )
                )
            except Tool.DoesNotExist:
                return PageNotFoundView.as_view()(
                    request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            u'URL contains unknown tool ID “{tool_id}“.',
                        )
                        .format(
                            tool_id=tool_id,
                        )
                    ),
                    status=400,
                )

        # --- Version ---
        version_arg = self.request.GET.get('version')
        if version_arg:
            version_arg_match = (
                re
                .match(VERSION_QUERY_STRING_ARG_PATTERN, version_arg)
            )

            if not version_arg_match:
                return PageNotFoundView.as_view()(
                    request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            u'URL contains unknown invalid version code “{version_code}“.',
                        )
                        .format(
                            version_code=version_arg,
                        )
                    ),
                    status=400,
                )

            version_arg_matches = version_arg_match.groupdict()
            version_tool_id = int(version_arg_matches.get('tool_id'))
            version_platform_slug = version_arg_matches.get('platform_slug')

            try:
                version = (
                    Version.objects
                    .get(
                        tool__id=version_tool_id,
                        supported_os__slug_name=version_platform_slug,
                    )
                )
            except Version.DoesNotExist:
                return PageNotFoundView.as_view()(
                    request,
                    error_message=(
                        pgettext(
                            u'Error message',
                            u'URL contains unknown version “{version_arg}“.',
                        )
                        .format(
                            version_arg=version_arg,
                        )
                    ),
                    status=400,
                )

        # ==============================
        # === Get and paginate posts ===
        # ==============================
        filter_args = {
            'language': self.request.LANGUAGE_CODE,
            'status': 'p'
        }
        if category:
            filter_args['category'] = category
        if is_featured:
            filter_args['homepage_feature__isnull'] = False

        # If both tool and version query string arguments are provided, posts
        # associated with the version and/or tool will be queried. It’s
        # necessary to do this because it’s possible that a post could be
        # tagged to a specific version without also being tagged to the
        # version’s tool

        tool_or_version_filter = Q()
        if tool and version:
            tool_or_version_filter = (
                Q(tool_tag=tool) |
                Q(version_tag=version)
            )
        elif tool:
            tool_or_version_filter = (
                Q(tool_tag=tool)
            )
        elif version:
            tool_or_version_filter = (
                Q(version_tag=version)
            )

        posts = (
            Post.objects
            .filter(
                tool_or_version_filter &
                Q(**filter_args)
            )
            .distinct()
            .order_by(order_by)
        )

        posts_paginator = Paginator(posts, POSTS_PER_PAGE)

        page_arg = self.request.GET.get('page', None)

        if page_arg == '1':
            query_string_args = deepcopy(self.request.GET)
            query_string_args.pop('page', None)

            url_without_page_arg = (
                self.request.build_absolute_uri(
                    self.request.path_info + '?' + query_string_args.urlencode()
                )
            )

            return redirect(
                url_without_page_arg,
                permanent=True
            )

        try:
            page = int(page_arg) if page_arg is not None else 1
            if page < 1:
                raise ValueError()

            current_page_posts = posts_paginator.page(page)
        except EmptyPage:
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        # Translators: Shown if a blog URL contains a “page”
                        # parameter that causes no posts to be returned.
                        u'There are no posts on this page.',
                    )
                    .format(
                        page_arg=page_arg
                    )
                )
            )
        except (InvalidPage, ValueError):
            return PageNotFoundView.as_view()(
                self.request,
                error_message=(
                    pgettext(
                        u'Error message',
                        u'URL contains invalid page value “{page_arg}”.',
                    )
                    .format(
                        page_arg=page_arg
                    )
                )
            )

        # ==============================================
        # === Construct next and previous page links ===
        # ==============================================
        next_page_link = None
        if current_page_posts.has_next():
            next_page_link_reverse_kwargs = (
                deepcopy(pagination_link_reverse_kwargs)
            )

            next_page_link_reverse_kwargs['q_page'] = (
                current_page_posts.next_page_number()
            )

            next_page_link = pask_reverse(
                'webfrontend:blogposts',
                self.request,
                **next_page_link_reverse_kwargs
            )

        previous_page_link = None
        if current_page_posts.has_previous():
            previous_page_link_reverse_kwargs = (
                deepcopy(pagination_link_reverse_kwargs)
            )

            previous_page_number = current_page_posts.previous_page_number()
            if previous_page_number != 1:
                previous_page_link_reverse_kwargs['q_page'] = (
                    previous_page_number
                )

            previous_page_link = pask_reverse(
                'webfrontend:blogposts',
                self.request,
                **previous_page_link_reverse_kwargs
            )

        # ================
        # === Metadata ===
        # ================
        meta_description = None
        if (
            category and
            category.description and
            not tool and
            not version
        ):
            meta_description = category.description
        else:
            meta_description = pgettext(
                u'Blog',
                # Translators: Description of the Paskoocheh blog. Provided text is
                # a placeholder! Should be short description of what the blog will
                # contain, suitable for search engine snippets and social media
                # previews.
                u'Description of Paskoocheh blog',
            )

        title_tool_name = None
        title_platform_locale_display_name = None

        if tool or version:
            tool = tool or version.tool

            tool_info = tool.infos.filter(
                language=self.request.LANGUAGE_CODE,
                publishable=True,
            ).first()

            title_tool_name = tool_info.name if tool_info else tool.name

        if version:
            title_platform_locale_display_name = version.supported_os.display_name_ar if app == 'zanga' else version.supported_os.display_name_fa

        category_name = get_localized_blog_category_name(category, request)

        page_title = get_blog_post_list_title(
            category_name=category_name,
            is_featured=is_featured,
            tool_name=title_tool_name,
            platform_locale_display_name=title_platform_locale_display_name,
        )

        view_metadata = PkViewMetadata(
            description=meta_description,
            title=page_title,
        )

        categories = Category.objects.annotate(num_post=Count('post')).filter(num_post__gt=0)

        # =========================================
        # === Read current filter search params ===
        # =========================================
        current_category_slug = None
        current_view_name = request.resolver_match.url_name

        query_string_args = request.GET
        if 'category' in query_string_args:
            current_category_slug = query_string_args['category']

        return render(
            self.request,
            'webfrontend/blogposts.html',
            context={
                'current_page_posts': current_page_posts,
                'is_blog_page': True,
                'next_page_link': next_page_link,
                'page_title': page_title,
                'pagination_link_reverse_kwargs': pagination_link_reverse_kwargs,
                'previous_page_link': previous_page_link,
                'view_metadata': view_metadata,
                'app': app,
                'categories': categories,
                'current_category_slug': current_category_slug,
                'current_view_name': current_view_name,
            }
        )
