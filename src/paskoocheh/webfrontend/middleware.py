import re
from copy import deepcopy
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.middleware import csrf
from django.utils.cache import add_never_cache_headers
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import npgettext, pgettext
from django.shortcuts import redirect
from functools import partial
from webfrontend.caches.utils import pattern_dict_to_pattern_glob
from webfrontend.utils.general import (
    enforce_required_args,
    get_ua_default_platform_slug_name_os,
    replace_wa_numerals_with_pa_numerals,
    SUPPORTED_PLATFORM_SLUG_NAMES,
)

u"""Webfrontend-specific middleware (registered globally by necessity)."""

STAT_KEY_PATTERN = re.compile(r'cache_type=stat_([\w_]+)&.*platform_slug_name=(\w+)&.*tool_id=(\d+)&')

app = settings.PLATFORM


class InterceptCsrfErrorMiddleware(object):
    u"""
    Middleware that renders an explanatory error message if user attempts to
    submit a form from client that doesn’t accept/send cookies.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        u"""
        If a client POSTs a form without sending cookies (e.g. if cookies are
        disabled), Django’s CSRF protection will respond with an
        HttpResponseForbidden because the csrftoken cookie is missing. We use
        this as well as the requested path to display an error message telling
        the user why they need to enable cookies to use the applicable feature.

        Args:
            https://docs.djangoproject.com/en/1.10/topics/http/middleware/

        Returns:
            HttpResponse
        """

        response = self.get_response(request)

        if (
            request.method == 'POST' and
            (
                hasattr(request, 'resolver_match') and
                hasattr(request.resolver_match, 'app_names') and
                request.resolver_match.app_names == ['webfrontend']
            ) and
            isinstance(response, HttpResponseForbidden)
        ):
            from webfrontend.views import PageNotFoundView

            if (request.resolver_match.url_name == 'setplatform'):
                # Translators: The user’s platform selection (the platform
                # chosen in the drop-down menu in the header) is saved as a
                # cookie. This error message appears if the browser doesn’t
                # support/allow cookies.
                error_message = pgettext(
                    u'Error message',
                    u'Paskoocheh requires cookies to save your platform selection. Please allow cookies from paskoocheh.com.'
                )
            elif (request.resolver_match.url_name == 'toolversion'):
                # Translators: A security feature in the backend requires the
                # user to have cookies enabled when submitting forms. This
                # error message appears if the browser doesn’t support/allow
                # cookies.
                error_message = pgettext(
                    u'Error message',
                    u'Paskoocheh requires cookies to accept reviews or support requests. Please allow cookies from paskoocheh.com.'
                )
            else:
                # Translators: This error message will appear if an action
                # other than saving the user’s platform selection fails because
                # the browser doesn’t support/allow cookies.
                error_message = pgettext(
                    u'Error message',
                    u'Paskoocheh requires cookies for this feature. Please allow cookies from paskoocheh.com.'
                )

            request.global_platform_slug = 'all'

            return PageNotFoundView.as_view()(
                request,
                error_message=error_message,
                status=400,
            )

        return response


class ResponseManipulationMiddleware(object):       # noqa C901
    u"""
    Middleware that manipulates webfrontend responses.
    """
    cache_versionratings = {}
    inline_style_tag_pattern = re.compile(r'(<style.*>(([^<]|\n)*)<\/style>)')
    stat_placeholder_pattern = re.compile(r'\[stat_([\w_]+)_(\d+)_(\w+)\]')
    versiondownload_none_translation = pgettext(
        u'Tool version download count',
        u'None',
    )
    versionrating_none_translation = pgettext(
        u'Tool version rating',
        u'None',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def get_stat_placeholder_replacement(self, match, request=None):        # noqa C901
        u"""
        Given a stat_placeholder_pattern match, get an appropriate response.

        Args:
            MatchObject (from stat_placeholder_pattern)

        Returns:
            Unicode
        """
        try:
            cache_type, tool_id, platform_slug_name = match.groups()
            placeholder = match.group()

            # For Zanga, replace values with Western Arabic numerals (e.g. 4.6)
            # For Paskoocheh, replace values with Perso-Arabic numerals (e.g. ۴.۶)

            if cache_type == 'versiondownload':
                if placeholder in request.webfrontend_stats['values_by_placeholder']:
                    download_count_numerals_comma_separated = None
                    if app == 'zanga':
                        download_count_numerals_comma_separated = str(request.webfrontend_stats['values_by_placeholder'][placeholder])
                    else:
                        download_count_numerals_comma_separated = (
                            replace_wa_numerals_with_pa_numerals(
                                '{:,}'.format(
                                    int(request.webfrontend_stats['values_by_placeholder'][placeholder])
                                )
                            )
                        )
                    return download_count_numerals_comma_separated
                else:
                    return self.versiondownload_none_translation
            elif cache_type == 'versionrating':
                if placeholder in request.webfrontend_stats['values_by_placeholder']:
                    rating_numerals = str(request.webfrontend_stats['values_by_placeholder'][placeholder])
                    return rating_numerals
                else:
                    return self.versionrating_none_translation
            elif cache_type == 'versionrating_count':
                rating_count = 0
                rating_count_comma_separated = 0

                if placeholder in request.webfrontend_stats['values_by_placeholder']:
                    rating_count = int(request.webfrontend_stats['values_by_placeholder'][placeholder])
                    rating_count_numerals_comma_separated = None
                    if app == 'zanga':
                        rating_count_numerals_comma_separated = rating_count
                    else:
                        rating_count_numerals_comma_separated = (
                            replace_wa_numerals_with_pa_numerals(
                                '{:,}'.format(
                                    rating_count
                                )
                            )
                        )
                    return (
                        npgettext(
                            u'Tool version',
                            u'{rating_count} rating',
                            u'{rating_count} ratings',
                            rating_count
                        )
                        .format(
                            rating_count=rating_count_numerals_comma_separated
                        )
                    )

                return (
                    # Translators: Rating count, displayed beneath rating in
                    # rating badge. Doesn’t need to be in brackets, as long as
                    # you think it will look good on the page. The translation
                    # for “ratings” should be terse if possible, since it needs
                    # to fit in a tight space.
                    npgettext(
                        u'Tool version',
                        u'{rating_count} rating',
                        u'{rating_count} ratings',
                        rating_count
                    )
                    .format(
                        rating_count=rating_count_comma_separated
                    )
                )

        except ValueError:
            pass

        return u'-'

    def __call__(self, request):
        u"""
        If the request was for a webfrontend view, manipulate the response:
        - Add Cache-Control: no-cache header
        - Replace [csrf_token] placeholders
        - Replace [stat_*] placeholders

        Args:
            https://docs.djangoproject.com/en/1.10/topics/http/middleware/

        Returns:
            HttpResponse
        """

        response = self.get_response(request)

        if (
            hasattr(request, 'resolver_match') and
            hasattr(request.resolver_match, 'app_names') and
            request.resolver_match.app_names == ['webfrontend']
        ):
            # ==========================================
            # === Add Cache-Control: no-cache header ===
            # ==========================================
            # See https://docs.djangoproject.com/en/1.11/topics/http/decorators/#django.views.decorators.cache.never_cache

            add_never_cache_headers(response)

            # =========================================
            # === Replace [csrf_token] placeholders ===
            # =========================================
            # Replace all insances of "[csrf_token]" with a request-specific
            # token. This is necessary because most views’ responses are
            # cached, and we need these caches to be shareable between
            # different clients. See README for more details.

            csrf_token_for_request = csrf.get_token(request).encode()

            response.content = response.content.replace(
                b'[csrf_token]',
                csrf_token_for_request
            )

            # =====================================
            # === Replace [stat_*] placeholders ===
            # =====================================
            # Replace all stat placeholders with values from
            # request.webfrontend_stats['values_by_placeholder'] (which is set in
            # RequestProcessingAndInterceptionMiddleware)

            response.content = re.sub(
                self.stat_placeholder_pattern,
                partial(self.get_stat_placeholder_replacement, request=request),
                response.content.decode(),
            ).encode()

            # ==============================
            # === Populate inline styles ===
            # ==============================

            inline_styles = u''

            # ------------------------------------------------
            # --- Hide Android promo notice if appropriate ---
            # ------------------------------------------------

            if (
                request.COOKIES.get('android_promo_notice_hidden') or
                'Android' not in request.headers['user-agent'] or
                'nocookies' in request.GET
            ):
                inline_styles += '''
                    .pk-android-promo-notice {
                        display: none;
                    }
                '''

            # -----------------------------------------------------------------
            # --- Gather all all <style> content into single <head> <style> ---
            # -----------------------------------------------------------------
            # Find and removes every <style> element, then consolidating the
            # contained styles into a single <style> element at the end of the
            # <head>.
            #
            # This is useful because it lets us calculate styles inside template
            # tags, which don’t have access to the outside context and therefore
            # can’t append styles to a global block. As of 2018-01-29, this is
            # currently only done in images_carousel.
            #
            # This is very much a hack, but less of a hack then trying to
            # pre-caculate styles outside of component template code to work
            # around the template tag isolation.

            style_element_matches = re.findall(self.inline_style_tag_pattern, response.content.decode())

            if style_element_matches:
                for style_element_match in style_element_matches:
                    # Group 0: Full style tag match ("<style>[…]</style>")
                    # Group 1: Inline styles (CSS)
                    # Group 2: Internal-use group, used to match newlines
                    if len(style_element_match) == 3:
                        inline_styles += style_element_match[1]
                        response.content = response.content.replace(
                            style_element_match[0].encode(),
                            b''
                        )

            if len(inline_styles) > 0:
                response.content = response.content.replace(
                    b'</head>',
                    b'<style type="text/css">' + inline_styles.encode() + b'</style>\n</head>'
                )

        return response


class RequestProcessingAndInterceptionMiddleware(MiddlewareMixin):
    u"""
    Middleware that runs before Django calls view.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        u"""
        Perform various tasks before Django calls view. In order:

        - Redirect to canonical scheme and host
        - Set request.canonical_url
        - Complete cookie availability test
        - Set global_platform cookie based on user agent

        Args:
            https://docs.djangoproject.com/en/1.10/topics/http/middleware/#process-view

        Returns:
            None (Django continues processing request)
            HttpResponseRedirect (intercept response with redirect before view
                is loaded)
        """
        # ================
        # === Bypasses ===
        # ================

        # Bypass middleware ASAP if not a webfrontend GET request
        if (
            request.method not in ['GET', 'POST'] or
            request.path.startswith('/__debug__') or
            request.path.startswith('/admin') or
            request.path.startswith('/api') or
            request.path.startswith('/jet') or
            request.path.startswith('/media') or
            request.path.startswith('/static') or
            request.path.startswith('/graphql') or
            request.path.startswith('/cms') or
            (
                request.headers.get('host') and
                request.headers.get('host').startswith('stats.')
            )
        ):
            return None

        # =============================================
        # === Redirect to canonical scheme and host ===
        # =============================================
        canonical_scheme = settings.WEBFRONTEND_CANONICAL_SCHEME
        canonical_host = settings.WEBFRONTEND_CANONICAL_HOST
        server_url = settings.SERVER_DIRECT_URL

        request_scheme = request.META.get('wsgi.url_scheme')
        request_host = request.headers.get('host')

        if (
            settings.WEBFRONTEND_ENFORCE_CANONICAL_SCHEME_AND_HOST and
            canonical_scheme and
            canonical_host and
            server_url and
            (
                request_scheme != canonical_scheme or
                request_host not in (server_url, canonical_host)
            )
        ):
            canonical_url = u'{canonical_scheme}://{canonical_host}{path}'.format(
                canonical_scheme=canonical_scheme,
                canonical_host=canonical_host,
                path=request.get_full_path(),
            )
            return redirect(canonical_url, permanent=True)

        # =================================
        # === Set request.canonical_url ===
        # =================================

        canonical_query_string_args = deepcopy(request.GET)
        canonical_query_string_args.pop('nocookies', None)

        request.canonical_url = (
            request.build_absolute_uri(
                request.path_info + '?' + canonical_query_string_args.urlencode()
            )
        )

        # ===============================================
        # === Get and validate global_platform cookie ===
        # ===============================================
        # If none of these conditions are matched, the response will be a
        # redirect that attempts to set the global_platform cookie.

        global_platform_cookie = request.COOKIES.get('global_platform')

        # If URL has ?nocookies and the cookie is in the request, the browser
        # supports cookies so we redirect to the same URL without ?nocookies
        if (
            'nocookies' in request.GET and
            global_platform_cookie is not None
        ):
            return redirect(request.canonical_url)

        # If URL has ?nocookies and the cookie isn’t in the request, the
        # browser doesn’t support cookies. The request is allowed to continue
        # with request.global_platform_slug set to 'all'
        if (
            'nocookies' in request.GET and
            global_platform_cookie is None
        ):
            request.global_platform_slug = 'all'

            # Populate request.webfrontend_stats from Redis cache
            self.populate_cache_stats(request)

            return None

        # Bypass middleware if global_platform cookie exists and is valid. The
        # request is allowed to continue with request.global_platform_slug set
        # to cookie value.
        if global_platform_cookie in SUPPORTED_PLATFORM_SLUG_NAMES:
            request.global_platform_slug = global_platform_cookie

            # Populate request.webfrontend_stats from Redis cache
            self.populate_cache_stats(request)

            return None

        # ======================================================
        # === Set global_platform cookie based on user agent ===
        # ======================================================
        # If process_view hasn’t returned yet, the global_platform cookie
        # should be set.

        # Get the most appropriate platform slug based on user agent
        platform_slug = get_ua_default_platform_slug_name_os(request)

        # Respond with redirect to the same page with nocookies query string
        # argument appended and global_platform Set-Cookie header included.
        # Note: If cookie name or duration changed, be sure to replicate in
        # SetPlatformView
        redirect_path = request.path_info
        if len(request.GET) > 0:
            redirect_path += ('?' + request.GET.urlencode() + '&nocookies')
        else:
            redirect_path += '?nocookies'

        response = redirect(redirect_path)
        response.set_cookie(
            httponly=True,
            key='global_platform',
            max_age=31536000,
            secure=True,
            value=platform_slug
        )

        return response

    def populate_cache_stats(self, request):
        u"""
        Populate request.webfrontend_stats from Redis cache. For efficiency’s
        sake, the cache is accessed once and shared throughout the request.

        It would be more efficient to store webfrontend_stats as a middleware
        attribute and keep it in memory between requests, however managing and
        refreshing this would introduce complexity and potential avenues for
        race conditions depending on the threading model on the server(?). If
        this turns out to be a performance issue, it would be worth looking at.

        Args:
            request (WSGIRequest)

        Returns:
            None
        """
        enforce_required_args(locals(), 'request')

        cache_stats = cache.get_many(
            cache.keys(
                pattern_dict_to_pattern_glob({
                    'cache_type': 'stat_*'
                })
            )
        )

        request.webfrontend_stats = {
            'values_by_placeholder': {},
            'versiondownload_values_by_key': {},
        }

        for cache_stat_key in cache_stats:
            match = re.search(STAT_KEY_PATTERN, cache_stat_key)

            if match:
                stat_cache_type, platform_slug_name, tool_id = match.groups()

                if stat_cache_type == 'versiondownload':
                    request.webfrontend_stats['versiondownload_values_by_key'][cache_stat_key] = (
                        cache_stats[cache_stat_key]
                    )

                placeholder = '[stat_{stat_cache_type}_{tool_id}_{platform_slug_name}]'.format(
                    stat_cache_type=stat_cache_type,
                    tool_id=tool_id,
                    platform_slug_name=platform_slug_name,
                )

                request.webfrontend_stats['values_by_placeholder'][placeholder] = (
                    cache_stats[cache_stat_key]
                )
