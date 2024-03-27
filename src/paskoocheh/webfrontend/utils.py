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

u"""webfrontend utilities.

Note that there are three different ways operating systems and/or browsers are
represented:

1. version_slug: Used in webfrontend URLs. They exist to create cleaner URLs,
   and to abstract away the internal supported_os so that URLs don’t break when
   the supported_os codes change. Should only be used when interpreting URL
   args or constructing a URL.

2. supported_os: Used in the Django data model to represent the platform
   (operating system or browser) of a tool version.

3. uap_info strings: Returned by ua_parser, the library we use to parse request
   user agents. Should not be retained internally.
"""

import attr
import icu
import logging
import re
import requests

from django.conf import settings
from django.core.cache import cache
from django.db.models import Case, Prefetch, Q, When
from django.urls import reverse
from django.utils.translation import npgettext, pgettext
from jdatetime import datetime as jdatetime
from operator import attrgetter
from preferences.models import ToolType
from tools.models import Image, Info, Version
from ua_parser import user_agent_parser
from urllib import urlencode
from webfrontend.caches.utils import pattern_dict_to_pattern_glob
from webfrontend.templatetags.tool_list_item import ToolListItemContext

VERSION_SLUG_TO_PLATFORM_NAME_MAPPINGS = {
    'all': None,
    'android': 'android',
    'ios': 'ios',
    'linux': 'linux',
    'linux32': 'linux32',
    'macos': 'macos',
    'windows': 'windows',
    'windows32': 'windows32',
    'chrome': 'chrome',
    'firefox': 'firefox',
    'windowsphone': 'windowsphone'
}
PLATFORM_NAME_TO_VERSION_SLUG_MAPPINGS = {
    'android': 'android',
    'ios': 'ios',
    'linux': 'linux',
    'linux32': 'linux32',
    'macos': 'macos',
    'windows': 'windows',
    'windows32': 'windows32',
    'chrome': 'chrome',
    'firefox': 'firefox',
    'windowsphone': 'windowsphone'
}

app = settings.PLATFORM

logger = logging.getLogger(__name__)


def pask_reverse(viewname, request, **kwargs):
    u"""
    Augmented replacement for Django’s django.urls.reverse that renders URLs
    with both path arguments (i.e. Django URL named group arguments) and query
    string arguments (which Django’s URL helpers don’t handle). Also includes
    “nocookies” query string argument when included in request.

    Path arguments should be prefixed with `p_`; query string arguments should
    be prefixed with `q_`.

    The arguments are prefixed and mixed rather than separated into
    dictionaries because this function is also wrapped as path_url template tag
    and template tags can’t take dict arguments. It would probably be confusing
    if pask_reverse and pask_url took different kwargs.

    e.g.:

    pask_reverse('webfrontend:toolversion', request,
        p_tool_id=1
        p_version_slug='android'
        q_foo='bar'
    )
    https://paskoocheh.com/tools/1/android?foo=bar

    Arguments:
        viewname (str): Django URL pattern name
        request (WSGIRequest)
        **kwargs: Mixed path and query string arguments

    Returns:
        path_and_query_string (str) (absolute path and query string, doesn’t
            include hostname)
    """
    path_args = {}
    query_string_args = {}

    for key in kwargs:
        if key.startswith('p_'):
            path_args[key.replace('p_', '')] = kwargs[key]
            continue
        elif key.startswith('q_'):
            query_string_args[key.replace('q_', '')] = kwargs[key]
            continue

    path_and_query_string = reverse(viewname, kwargs=path_args)

    if len(query_string_args) > 0:
        if 'nocookies' in request.GET:
            path_and_query_string += (
                '?' + urlencode(query_string_args) + '&nocookies'
            )
        else:
            path_and_query_string += ('?' + urlencode(query_string_args))
    elif 'nocookies' in request.GET:
        path_and_query_string += '?nocookies'

    return path_and_query_string


def get_prefixed_query_string_args(query_string_args):
    u"""
    Returns a dict of query string args (probably from request.GET or
    context['request'].GET) with all keys prefixed with “q_”, for
    use in pask_reverse.

    Args:
        query_string_args (dict)

    Returns:
        dict
    """

    prefixed_query_string_args = {}
    for arg_key in query_string_args:
        prefixed_query_string_args['q_' + arg_key] = query_string_args[arg_key]

    return prefixed_query_string_args


def populate_request_uap_info(request):
    u"""Populate request.uap_info if it isn’t already set.

    If request.uap_info isn’t set, sends request’s user agent to ua_parser and
    sets request.uap_info. This is to avoid redundant parsing.

    Args:
        request (WSGIRequest)

    Returns:
        uap_info (dict)
        (Not necessary since uap_info is also populated
        in request, but returned to avoid surprise.)
    """
    if not hasattr(request, 'uap_info'):
        request.uap_info = (
            user_agent_parser.Parse(request.headers['user-agent'])
        )

    return request.uap_info


def get_filter_version_slugs(primary_version_slug):
    u"""
    Returns an array of version slugs to be used in tool query. If the
    primary version is a desktop OS, Chrome and Firefox are appended;
    otherwise, it just contains the primary version.

    Args:
        primary_version_slug (str): Version slug of the query

    Returns:
        filter_version_slugs (array): Array containing all version slugs to be
        queried (probably used as the value of a
        versions__supported_os__slug_name__in kwarg)
    """
    filter_version_slugs = [
        VERSION_SLUG_TO_PLATFORM_NAME_MAPPINGS[primary_version_slug]
    ]

    if primary_version_slug in ['linux', 'macos', 'windows']:
        filter_version_slugs.extend(['chrome', 'firefox'])

    return filter_version_slugs


def get_preferred_supported_os_name_ordering_case(preferred_supported_os_name_order):
    u"""
    Returns a Case that can be used to order Version instances by
    preferred_supported_os_name_order.

    GH: I don’t know SQL well enough to fully understand how this works, but it
    has the effect of ordering the versions by the
    preferred_supported_os_name_order. I assume doing this via SQL is more
    efficient than sorting the data in Python.

    Via https://stackoverflow.com/a/38390480/7949868
    """
    return Case(
        *[
            When(supported_os__slug_name=order_supported_os, then=order_index)
            for order_index, order_supported_os
            in enumerate(preferred_supported_os_name_order)
        ]
    )


def add_select_related_to_faqs_queryset(faqs_queryset):
    u"""
    Returns the given QuerySet with tool, version, and version.supported_os
    (Platform) selected

    Args:
        faqs_queryset (QuerySet): QuerySet for tools.models.Faq entities

    Returns:
        faqs_queryset_with_related_selected (QuerySet)
    """
    faqs_queryset_with_related_selected = (
        faqs_queryset
        .select_related('tool', 'version', 'version__supported_os')
    )

    return faqs_queryset_with_related_selected


def add_select_related_to_tutorials_queryset(tutorials_queryset):
    u"""
    Returns the given QuerySet with version, and version.supported_os
    (Platform) selected

    Args:
        tutorials_queryset (QuerySet): QuerySet for tools.models.Tutorial
        entities

    Returns:
        tutorials_queryset_with_related_selected (QuerySet)
    """
    tutorials_queryset_with_related_selected = (
        tutorials_queryset
        .select_related('version', 'version__supported_os')
    )

    return tutorials_queryset_with_related_selected


def add_prefetch_related_to_tools_queryset(tools_queryset, request, preferred_supported_os=None):
    u"""
    Returns the given QuerySet with publishable versions and logo images
    preloaded. Versions are preferentially ordered based on the request’s user
    agent.

    Args:
        tools_queryset (QuerySet): QuerySet for tools, probably from index or
            search controllers
        request (WSGIRequest)

    Returns:
        tools_queryset_with_prefetches (QuerySet)
    """
    preferred_supported_os_name_order = (
        get_preferred_supported_os_name_order(request, preferred_supported_os)
    )

    preferred_supported_os_name_ordering_case = (
        get_preferred_supported_os_name_ordering_case(
            preferred_supported_os_name_order
        )
    )

    versions_queryset = (
        Version.objects
        .filter(
            publishable=True,
        )
        .order_by(
            preferred_supported_os_name_ordering_case
        )
    )

    tools_queryset_with_prefetches = (
        tools_queryset.prefetch_related(
            Prefetch(
                'versions',
                queryset=versions_queryset,
            )
        )
        # TODO: It would be slightly more efficient if this only fetched the
        # necessary platforms instead of always getting them all, but it
        # doesn’t seem to be easy to do. It’s already a fast query, so not a
        # big deal.
        .prefetch_related(
            Prefetch(
                'versions__supported_os',
            )
        ).prefetch_related(
            Prefetch(
                'images',
                queryset=(
                    Image.objects
                    .filter(
                        Q(image_type='logo') &
                        (
                            Q(language__isnull=True) |
                            Q(language=request.LANGUAGE_CODE)
                        ) &
                        Q(publish=True)
                    )
                    .order_by('order')
                ),
                to_attr='logo_images',
            )
        ).prefetch_related(
            Prefetch(
                'infos',
                queryset=Info.objects.filter(
                    language=request.LANGUAGE_CODE,
                    publishable=True,
                ),
                to_attr='infos_current_language',
            )
        )
    )

    return tools_queryset_with_prefetches


def get_tool_types_queryset():
    u"""
    Returns a queryset containing all ToolTypes except “Uncategorized tools”

    Returns:
        tool_types (QuerySet)
    """

    tool_types = (
        ToolType.objects
        .exclude(
            name='Uncategorized tools'
        )
        .order_by('name')
    )

    return tool_types


def get_ua_default_platform_name_os(request):
    u"""Get the request user agent’s Platform name.

    Only returns operating systems, not 'chrome' or 'firefox'

    Args:
        request (WSGIRequest)

    Returns:
        platform_name (str)
    """
    populate_request_uap_info(request)

    ua_os = request.uap_info['os']['family']

    if ua_os == 'Windows Phone':
        return 'windowsphone'
    elif ua_os == 'Android':
        return 'android'
    elif ua_os == 'iOS':
        return 'ios'
    elif ua_os == 'Linux':
        return 'linux'
    elif ua_os == 'Mac OS X':
        return 'macos'
    elif 'Windows' in ua_os:
        return 'windows'

    return 'android'


def get_ua_default_version_slug_os(request):
    ua_default_platform_slug_name_os = get_ua_default_platform_name_os(request)

    return PLATFORM_NAME_TO_VERSION_SLUG_MAPPINGS[ua_default_platform_slug_name_os]


def get_preferred_supported_os_name_order(request, preferred_platform_slug_name_os=None):
    u"""
    Get a preferred order of supported_os based on several factors.

    Starts with a default hard-coded preferred order of supported_os strings
    (based on popularity). If a preferred_supported_os is provided, it’s pushed
    to the top of the list; otherwise, a preferred_supported_os is chosen based
    on the request’s user agent.

    Args:
        request (WSGIRequest)

    Returns:
        preferred_supported_os_name_order (list)
    """

    # Initial order is based on the platform download popularity. Chrome and
    # Firefox pushed to top if preferred platform is desktop.
    if preferred_platform_slug_name_os in ['linux', 'macos', 'windows']:
        preferred_platform_slug_order = [
            'chrome',
            'firefox',
            'android',
            'windows',
            'ios',
            'macos',
            'linux',
            'windowsphone',
            'linux32',
            'windows32',
        ]
    else:
        preferred_platform_slug_order = [
            'android',
            'windows',
            'ios',
            'chrome',
            'firefox',
            'macos',
            'linux',
            'windowsphone',
            'linux32',
            'windows32',
        ]

    if preferred_platform_slug_name_os is None:
        preferred_platform_slug_name_os = get_ua_default_platform_name_os(request)

    if not preferred_platform_slug_name_os:
        return preferred_platform_slug_order

    try:
        preferred_platform_slug_order.insert(
            0,
            preferred_platform_slug_order.pop(
                preferred_platform_slug_order.index(preferred_platform_slug_name_os)
            )
        )
    except ValueError:
        logger.warning(
            u'Something went wrong while attempting to reorder preferred_platform_slug_order.'
        )

    return preferred_platform_slug_order


def get_tool_preferred_version_path(tool, request):
    preferred_supported_os_name = None

    if (
        hasattr(request, 'global_version_slug') and
        request.global_version_slug != 'all'
    ):
        preferred_supported_os_name = request.global_version_slug

    preferred_supported_os_name_order = (
        get_preferred_supported_os_name_order(request, preferred_supported_os_name)
    )

    preferred_supported_os_name_ordering_case = (
        get_preferred_supported_os_name_ordering_case(
            preferred_supported_os_name_order
        )
    )

    version = (
        Version.objects
        .filter(
            publishable=True,
            tool=tool,
        )
        .order_by(preferred_supported_os_name_ordering_case)
        .first()
    )

    if version is not None:
        return pask_reverse(
            'webfrontend:toolversion',
            request,
            p_tool_id=tool.id,
            p_version_slug=version.supported_os.name,
        )
    else:
        return None


def verify_request_grecaptcha(request):
    u"""
    Send the POST `g-recaptcha-response` argument to Google for verification,
    return the validity.

    Args:
        request (WSGIRequest)

    Returns:
        reCAPTCHA validity (bool)
    """
    if 'g-recaptcha-response' not in request.POST:
        logger.error(
            u'Couldn’t verify reCAPTCHA because request was missing required g-recaptcha-response POST argument.'
        )
        return False

    if 'grecaptcha-type' not in request.POST:
        logger.error(
            u'Couldn’t verify reCAPTCHA because request was missing required grecaptcha-type POST argument.'
        )
        return False

    recaptcha_response = request.POST['g-recaptcha-response']
    grecaptcha_secret = None

    if request.POST['grecaptcha-type'] == 'invisible':
        grecaptcha_secret = settings.GRECAPTCHA_INVISIBLE_SECRET
    elif request.POST['grecaptcha-type'] == 'v2':
        grecaptcha_secret = settings.GRECAPTCHA_V2_SECRET

    if not grecaptcha_secret:
        logger.error(
            u'Couldn’t verify reCAPTCHA because corresponding secret key couldn’t be determined.'
        )
        return False

    verification_response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify', {
            'secret': grecaptcha_secret,
            'response': recaptcha_response
        }
    )
    verification_response_json = verification_response.json()

    if (
        'success' in verification_response_json and
        verification_response_json['success'] is True
    ):
        return True

    return False


@attr.s(frozen=True, slots=True)
class VideoMetadata(object):
    u"""
    Immutable object containing metadata about a video URL.

    Attributes:
        video_type ('youtube', 'vimeo', 'file', or None if no match)
        external_video_id (str or None): Video ID for external service, or
            None if no match
    """
    external_id = attr.ib()
    type = attr.ib()


def parse_video_url(video_url):
    u"""
    Parses a video URL, returns the video type and external service (YouTube, Vimeo) video ID

    Args:
        video_url (str): Video

    Returns:
        webfrontend.utils.VideoMetadata
    """
    import re

    youtube_video_id_matches = re.match(
        r'https:\/\/www\.youtube\.com\/watch\?.*v=([^&]*)',
        video_url
    )

    if (youtube_video_id_matches):
        return VideoMetadata(
            external_id=youtube_video_id_matches.group(1),
            type='youtube',
        )

    vimeo_video_id_matches = re.match(
        r'https:\/\/vimeo\.com\/(\d+).*',
        video_url
    )

    if (vimeo_video_id_matches):
        return VideoMetadata(
            external_id=vimeo_video_id_matches.group(1),
            type='vimeo',
        )

    return VideoMetadata(
        external_id=None,
        type=None,
    )


def construct_tool_list_item_context_list(  # noqa: C901
    order_by=None,
    order_reverse=False,
    request=None,
    stats_for_platform_slug_name=None,
    tools=None,
):
    u"""
    Processes a list of tools into a list of ToolListItemContext ordered by
    order_by, or by transliterated name if no order provided.

    Required args:
        request (WSGIRequest)
        stats_for_platform_slug_name (str): Platform name to use when querying
            stats. To get aggregate stats, use “all”. Affects displayed stats
            as well as download_count ordering.
        tools (iterable of Tool)

    Optional args:
        order_by (str): ToolListItemContext sorting key
        order_reverse (bool): Reverse sorting order?

    Returns:
        list of ToolListItemContext
    """
    enforce_required_args(locals(), 'request', 'stats_for_platform_slug_name', 'tools')

    # ==============================================
    # === Get version download counts from cache ===
    # ==============================================
    cache_versiondownload_keys = cache.keys(
        pattern_dict_to_pattern_glob({
            'cache_type': 'stat_versiondownload',
            'platform_slug_name': stats_for_platform_slug_name,
        })
    )

    cache_versiondownloads = cache.get_many(cache_versiondownload_keys)

    # =============================================
    # === Build list of tool_list_item_context  ===
    # =============================================
    tool_list_item_contexts = []

    for tool in tools:
        # Don’t include tool if it isn’t publishable or has no (publishable)
        # versions
        if tool.publishable is False or tool.versions.count() == 0:
            continue

        # tool.logo_images is populated by prefetch_related in the main view
        if (
            hasattr(tool, 'logo_images') and
            len(tool.logo_images) > 0
        ):
            logo = tool.logo_images[0]
        else:
            logo = None

        # To get the first tool version (which is the one we display, since the
        # list is preferentially ordered in the query), it’s faster to use
        # tool.versions.all()[0] rather than tool.versions.first() because the
        # result of .all() is already prefetched in memory.
        version = tool.versions.all()[0]
        platform_slug = (
            PLATFORM_NAME_TO_VERSION_SLUG_MAPPINGS[version.supported_os.slug_name]
        )

        # -----------------------------------------------------------------
        # --- Figure out if a browser version badge should be displayed ---
        # -----------------------------------------------------------------
        current_view_name = request.resolver_match.url_name

        should_display_browser_badge = (
            current_view_name in ['index', 'search'] and
            platform_slug in ['chrome', 'firefox'] and
            'platform' in request.GET and
            request.GET['platform'] in ['linux', 'macos', 'windows']
        )

        # ---------------------
        # --- Get tool name ---
        # ---------------------
        tool_info = None
        if (
            hasattr(tool, 'infos_current_language') and
            len(tool.infos_current_language) > 0
        ):
            tool_info = tool.infos_current_language[0]

        if tool_info is not None:
            name = tool_info.name
        else:
            name = tool.name

        # ---------------------------------------------------
        # --- Find version download count in cache values ---
        # ---------------------------------------------------
        download_count = 0
        for key in cache_versiondownloads:
            if (
                'tool_id={}&'.format(tool.id) in key and
                'platform_slug_name={}&'.format(stats_for_platform_slug_name) in key
            ):
                download_count = int(cache_versiondownloads[key])
                break

        should_display_all_platform_stats = (
            stats_for_platform_slug_name == 'all'
        )

        # ----------------------------------------
        # --- Construct tool list item context ---
        # ----------------------------------------
        tool_list_item_contexts.append(
            ToolListItemContext(
                download_count=download_count,
                logo=logo,
                name=name,
                platform_slug=platform_slug,
                should_display_browser_badge=should_display_browser_badge,
                should_display_all_platform_stats=should_display_all_platform_stats,
                version=version,
            )
        )

    if order_by:
        sorted_tool_list_item_contexts = (
            sorted(
                tool_list_item_contexts,
                key=attrgetter(order_by),
                reverse=order_reverse
            )
        )
    else:
        icu_transliterator = icu.Transliterator.createInstance('Arabic-Latin/BGN' if app == 'zanga' else 'Persian-Latin/BGN')

        sorted_tool_list_item_contexts = (
            sorted(
                tool_list_item_contexts,
                key=lambda tool_list_item: icu_transliterator.transliterate(tool_list_item.name)
            )
        )

    return sorted_tool_list_item_contexts


@attr.s(frozen=True, slots=True)
class ReviewFormRatingOption(object):
    u"""
    Immutable object describing a review form rating <option>.

    Attributes:
        text (str): Localized textual description of rating (e.g. '3 stars')
        value (float)
    """
    text = attr.ib()
    value = attr.ib()


def get_rating_options():
    u'''
    Generates a list of ReviewFormRatingOption, including translated text
    values.

    Returns:
        list of ReviewFormRatingOption
    '''
    rating_options = []
    for i in range(11):
        rating = float(i) / 2

        rating_options.append(
            ReviewFormRatingOption(
                text=(
                    npgettext(
                        u'Review',
                        # Translators: Selections in the review form rating
                        # drop-down
                        u'{rating} star',
                        u'{rating} stars',
                        rating
                    )
                    .format(
                        rating=rating
                    )
                ),
                value=rating,
            )
        )

    return rating_options


def wrap_with_link(text, href):
    u"""
    Returns provided text wrapped in anchor tag with provided href.

    Args:
        text (str): Text to be wrapped
        href (str): href value of wrapping link
    """
    return '{link_open}{text}{link_close}'.format(
        link_open=(
            u'<a class="inline-link" href="{href}">'.format(
                href=href
            )
        ),
        text=text,
        link_close=u'</a>',
    )


def get_blog_post_list_title(**kwargs):
    u"""
    Returns a translated tool list title based on the provided kwargs.

    Args:
        Optional:
            category_name (unicode)
            is_featured (bool)
                True if list is limited to featured tools. False is unsupported.
            platform_name (unicode)
            tool_name (unicode)

    Returns:
        Unicode string
    """
    category_name = kwargs.get('category_name', None)
    is_featured = kwargs.get('is_featured', False)
    platform_name = kwargs.get('platform_name', None)
    tool_name = kwargs.get('tool_name', None)

    if platform_name and not tool_name:
        raise TypeError('If platform_name is provided, tool_name must be set')

    title = None

    featured_translation = pgettext(
        u'List title',
        u'Featured',
    )

    if tool_name and platform_name:
        title = (
            pgettext(
                u'Blog post list title',
                # Translators: Used for blog post list titles (e.g. on the blog
                # homepage, category pages, etc.). Note that the variables can
                # be reordered as you see fit – the tranlsation system is
                # designed to allow different ordering/formatting for different
                # languages.
                u'{featured} {category_name} blog posts about {tool_name} for {platform_name}'
            )
            .format(
                category_name=category_name or '',
                featured=(
                    featured_translation if is_featured else ''
                ),
                tool_name=tool_name,
                platform_name=platform_name,
            )
        )
    elif tool_name:
        title = (
            pgettext(
                u'Blog post list title',
                # Translators: Used for blog post list titles (e.g. on the blog
                # homepage, category pages, etc.). Note that the variables can
                # be reordered as you see fit – the tranlsation system is
                # designed to allow different ordering/formatting for different
                # languages.
                u'{featured} {category_name} blog posts about {tool_name}'
            )
            .format(
                category_name=category_name or '',
                featured=(
                    featured_translation if is_featured else ''
                ),
                tool_name=tool_name,
            )
        )
    elif category_name or is_featured:
        title = (
            pgettext(
                u'Blog post list title',
                # Translators: Used for blog post list titles (e.g. on the blog
                # homepage, category pages, etc.). Note that the variables can
                # be reordered as you see fit – the tranlsation system is
                # designed to allow different ordering/formatting for different
                # languages.
                u'{featured} {category_name} blog posts'
            )
            .format(
                category_name=category_name or '',
                featured=(
                    featured_translation if is_featured else ''
                ),
            )
        )
    else:
        title = (
            pgettext(
                u'Blog post list title',
                # Translators: Used for blog post list titles (e.g. on the blog
                # homepage, category pages, etc.). Note that the variables can
                # be reordered as you see fit – the tranlsation system is
                # designed to allow different ordering/formatting for different
                # languages.
                u'Latest blog posts'
            )
        )

    # Remove leading or trailing spaces
    title = re.sub(r'(^\s+|\s+$)', u'', title)

    # Remove extra interior spaces
    title = re.sub(r'(\s{2,})', u' ', title)

    return title


def get_tool_list_title(**kwargs):
    u"""
    Returns a translated tool list title based on the provided kwargs.

    Args:
        **kwargs:
            is_featured (bool): True if list is limited to featured tools
            is_for_other_platforms (bool): True if the list contains tools for
                other platforms (used in SearchView)
            order_by_slug (str): Slug code describing order of list (same as
                `orderby` SearchView GET argument)
            platform_name (str): Platform.name (translated)
            query (str): Raw search query
            tool_type_name (str): ToolType.name (translated)

    Returns:
        Unicode string
    """

    # ===================
    # === Read kwargs ===
    # ===================

    is_featured = kwargs.get('is_featured', False)
    is_for_other_platforms = kwargs.get('is_for_other_platforms', False)
    order_by_slug = kwargs.get('order_by_slug', None)
    platform_name = kwargs.get('platform_name', None)
    query = kwargs.get('query', None)
    tool_type_name = kwargs.get('tool_type_name', None)

    # ==========================
    # === Gather format args ===
    # ==========================

    featured_translation = None
    if is_featured:
        featured_translation = pgettext(
            u'List title',
            # Translators: Feeds into blog/tool list title {featured} fields
            u'Featured'
        )

    description_translation = None
    if order_by_slug:
        if order_by_slug == u'downloadcount':
            description_translation = pgettext(
                u'Tool list title description',
                # Translators: Used in tool list titles on homepage, category
                # pages, and search pages. Feeds into tool list title
                # {description} fields.
                u'Most downloaded'
            )
        elif order_by_slug == u'dateadded':
            description_translation = pgettext(
                u'Tool list title description',
                # Translators: Used in tool list titles on homepage, category
                # pages, and search pages. Feeds into tool list title
                # {description} fields.
                u'Recently added'
            )
        elif order_by_slug == u'dateupdated':
            description_translation = pgettext(
                u'Tool list title description',
                # Translators: Used in tool list titles on homepage, category
                # pages, and search pages. Feeds into tool list title
                # {description} fields.
                u'Recently updated'
            )

    format_args = {
        'featured': (featured_translation if is_featured else ''),
        'description': (description_translation or ''),
        'query': (query or ''),
        'tool_type': (tool_type_name or ''),
        'platform': (platform_name or ''),
    }

    # =========================================
    # === Translate and format title string ===
    # =========================================

    if is_for_other_platforms:
        title = (
            pgettext(
                u'Tool list title',
                # Translators: Used for the “for other platforms” list that
                # appears in search views. The list includes all tools that
                # don’t have a version for the requested platform. Note that
                # the variables can be reordered as you see fit – the
                # tranlsation system is designed to allow different
                # ordering/formatting for different languages.
                u'{description} {featured} “{query}” {tool_type} tools for other platforms'
            )
            .format(**format_args)
        )
    elif platform_name and platform_name != 'all':
        title = (
            pgettext(
                u'Tool list title',
                # Translators: Used for tool lists with an associated platform.
                # This string is provided separately from the non-platform-
                # specific string to give you more formatting flexibility. Note
                # that the variables can be reordered as you see fit – the
                # tranlsation system is designed to allow different
                # ordering/formatting for different languages.
                u'{description} {featured} “{query}” {tool_type} tools for {platform}'
            )
            .format(**format_args)
        )
    else:
        title = (
            pgettext(
                u'Tool list title',
                # Translators: Used for tool lists without an associated
                # platform (i.e. if the global platform is “All tools”). This
                # string is provided separately from the non-platform-specific
                # string to give you more formatting flexibility. Note that the
                # variables can be reordered as you see fit – the tranlsation
                # system is designed to allow different ordering/formatting for
                # different languages.
                u'{description} {featured} “{query}” {tool_type} tools'
            )
            .format(**format_args)
        )

    # =============================
    # === Clean up title string ===
    # =============================

    # Remove quotation marks if query ended up being blank
    title = re.sub(r'(“”|”“|\"\"|‘’|’‘|\'\')', u'', title)

    # Remove leading or trailing spaces
    title = re.sub(r'(^\s+|\s+$)', u'', title)

    # Remove extra interior spaces
    title = re.sub(r'(\s{2,})', u' ', title)

    return title


def enforce_required_args(args_dict, *required_arg_names):
    u"""
    Raise a TypeError if any argument name in required_arg_names is missing
    from (or has a value of None in) args_dict. Used to enforce required named
    arguments. There are betters ways of achieving this in Python 3.x.

    Args:
        args_dict (dict): A dictionary of arguments. Should be the return value
            of locals() called before any local variables are defined.
        *required_arg_names (str)

    Returns:
        None (raises TypeError otherwise)
    """
    for arg_name in required_arg_names:
        if args_dict.get(arg_name) is None:
            raise TypeError(
                'Missing a required argument {arg_name}.'.format(
                    arg_name=arg_name
                )
            )

    return None


def is_request_user_agent_noop(request):
    u"""
    Determine if a request should be considered noop based on its user agent.

    If the request’s user agent matches any of the patterns in
    NOOP_USER_AGENT_PATTERNS it’s considered noop. Any function that results in
    data being stored (analytics, forms, etc.) should use this function and
    short-circuit (probably returning a 403 error) if it returns True.

    Args:
        request (WSGIRequest)
    Returns:
        bool
    """
    if hasattr(request, 'is_noop'):
        return request.is_noop

    request_user_agent = request.headers.get('user-agent', '')

    if any(noop_regex.match(request_user_agent) for noop_regex in settings.NOOP_USER_AGENT_PATTERNS):
        request.is_noop = True
        return True

    request.is_noop = False
    return False


def gregorian_datetime_to_jalali_date_string(gregorian_datetime):
    u"""
    Convert a gregorian datetime to a Jalali short date string.

    Args:
        gregorian_datetime (datetime)
    Returns:
        str
    """
    jalali_date_string = (
        jdatetime.fromgregorian(datetime=gregorian_datetime)
        .strftime(u'%Y/%M/%d')
    )

    return jalali_date_string


def get_localized_blog_category_name(category, request):
    u"""
    Get the name of the provided blog category in the current language.

    Args:
        category (blog.models.Category)
        request (WSGIRequest)
    Returns:
        unicode
    """
    if not category:
        return None

    category_name = getattr(category, 'name', None)

    if request.LANGUAGE_CODE == 'ar' and category.name_ar:
        category_name = category.name_ar
    elif request.LANGUAGE_CODE == 'fa' and category.name_fa:
        category_name = category.name_fa

    return category_name


def image_exists(imagefile):
    u"""
    Tries to determine if an ImageFile exists without needing to open it.

    This is done by checking for the existence of height and width attributes,
    which is a hack that may stop working if Django’s behaviour changes.

    TODO: Use this to consolidate image verification across webfrontend.

    Args:
        imagefile (django.core.files.images.ImageFile)
    Returns:
        unicode
    """

    return (
        imagefile and
        hasattr(imagefile, 'height') and
        hasattr(imagefile, 'width')
    )
