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

u"""Registers toolversion_main Django template tag."""

from blog.models import Post
from django import template
from django.db.models import Q
from tools.models import Faq, Guide, Tutorial, Tool
from webfrontend.utils.general import (
    enforce_required_args,
    replace_wa_numerals_with_pa_numerals,
)
from webfrontend.utils.query import (
    add_select_related_to_faqs_queryset,
    add_select_related_to_tutorials_queryset,
)
from django.conf import settings
from django.utils import translation
from webfrontend.utils.uri import pask_reverse

register = template.Library()

app = settings.PLATFORM


@register.inclusion_tag(
    'webfrontend/tags/toolversion_main.html',
    takes_context=True
)
def toolversion_main(             # noqa C901
    context,
    display_review_success=False,
    display_support_success=False,
    tool=None,
    tool_info=None,
    tool_logo=None,
    tool_name_localized=None,
    tool_screenshots=None,
    tool_version=None,
    tool_versions=None,
    version_name_localized=None,
):
    u"""
    Build the context for the toolversion_main inclusion tag.

    Required args:
        tool (Tool)
        tool_info (Info)
        tool_name_localized (unicode)
        tool_screenshots (iterable of Image)
        tool_version (Version)
        tool_versions (iterable of Versions)
        version_name_localized (unicde)

    Optional args:
        tool_logo (Image)
        display_review_success
        display_support_success

    Returns:
        dictionary: Template context
    """
    enforce_required_args(
        locals(),
        'tool',
        'tool_name_localized',
        'tool_screenshots',
        'tool_version',
        'tool_versions',
        'version_name_localized',
    )

    # =========================================
    # === Reformat release date for display ===
    # =========================================
    # e.g.: "1395-06-10 15:31:07" -> "1395/06/10"

    tool_version_formatted_release_jdate = (
        replace_wa_numerals_with_pa_numerals(tool_version.release_jdate)
    )

    # ========================
    # === Get first 5 FAQs ===
    # ========================
    # Gets the first 5 FAQs for this version, or for this version’s tool (but
    # not for a different version of the tool)

    version_faqs = add_select_related_to_faqs_queryset(
        Faq.objects
        .filter(
            Q(publishable=True) &
            Q(language=context.request.LANGUAGE_CODE) &
            (
                (
                    Q(version=tool_version)
                ) |
                (
                    Q(tool=tool) &
                    Q(version=None)
                )
            )
        )
        .order_by('order')
        [:5]
    )

    # =========================================
    # === Figure out if version has a guide ===
    # =========================================
    tool_version_has_guide = False
    try:
        (
            Guide.objects
            .filter(
                language=context.request.LANGUAGE_CODE,
                publishable=True,
                version=tool_version,
            )
            [0:1]
            .get()
        )

        tool_version_has_guide = True
    except Guide.DoesNotExist:
        pass

    # =====================================
    # === Get first 5 version tutorials ===
    # =====================================
    version_tutorials = add_select_related_to_tutorials_queryset(
        Tutorial.objects
        .filter(
            language=context.request.LANGUAGE_CODE,
            publishable=True,
            version=tool_version
        )
        .order_by('order')
        [:5]
    )

    # ================================================
    # === TODO Get first 3 related tools/versions  ===
    # ================================================
    tags_list = list(tool.tags.values_list('slug', flat=True))
    related_tools = (
        Tool.objects
        .filter(
            Q(publishable=True) &
            Q(tags__slug__in=tags_list)
        )
        .exclude(pk=tool.pk)
        .order_by('-last_modified')
        [:3]
    )

    # ===========================================
    # === Get first 5 tool/version blog posts ===
    # ===========================================
    version_blog_posts = (
        Post.objects
        .filter(
            Q(language=context.request.LANGUAGE_CODE) &
            Q(status='p') &
            (
                (
                    Q(tool_tag=tool) &
                    Q(version_tag=None)
                ) |
                (
                    Q(version_tag=tool_version)
                )
            )
        )
        .distinct()
        .order_by('-published_date')
        [:5]
    )

    # ======================================================
    # === If platform is Linux, get 32-bit linux version ===
    # ======================================================
    # Because 32-bit Linux (linux32) versions aren’t exposed, get the 32-bit
    # version so that its download links can be displayed beside the 64-bit
    # download links.

    linux32_version = None

    if tool_version.supported_os.slug_name == 'linux':
        for version in tool_versions:
            if version.supported_os.slug_name == 'linux32':
                linux32_version = version
                break

    # ==========================================================
    # === If platform is Windows, get 32-bit windows version ===
    # ==========================================================
    # Because 32-bit Windows (windows32) versions aren’t exposed, get the 32-bit
    # version so that its download links can be displayed beside the 64-bit
    # download links.

    windows32_version = None

    if tool_version.supported_os.slug_name == 'windows':
        for version in tool_versions:
            if version.supported_os.slug_name == 'windows32':
                windows32_version = version
                break

    # ===============================================
    # === Generate stats cache value placeholders ===
    # ===============================================
    versiondownload_cache_placeholder = (
        '[stat_versiondownload_{tool_id}_{platform_slug_name}]'.format(
            tool_id=tool_version.tool.id,
            platform_slug_name=tool_version.supported_os.slug_name,
        )
    )

    versionrating_cache_placeholder = (
        '[stat_versionrating_{tool_id}_{platform_slug_name}]'.format(
            tool_id=tool_version.tool.id,
            platform_slug_name=tool_version.supported_os.slug_name,
        )
    )

    versionrating_count_cache_placeholder = (
        '[stat_versionrating_count_{tool_id}_{platform_slug_name}]'.format(
            tool_id=tool_version.tool.id,
            platform_slug_name=tool_version.supported_os.slug_name,
        )
    )

    # ======================================================
    # === Get verstion rating value from the stats cache ===
    # ======================================================
    # Get the cached value and localize it only for Paskoocheh
    # using Perso-Arabic numerals since Zanga will use
    # the placeholder as is (WA numerals)

    version_rating = versionrating_cache_placeholder

    if versionrating_cache_placeholder in context['request'].webfrontend_stats['values_by_placeholder'] and app != 'zanga':
        version_rating = (
            replace_wa_numerals_with_pa_numerals(
                '{:}'.format(
                    float(context['request'].webfrontend_stats['values_by_placeholder'][versionrating_cache_placeholder])
                )
            )
        )

    no_version_rating_available = True
    if versionrating_cache_placeholder in context.request.webfrontend_stats['values_by_placeholder']:
        no_version_rating_available = False

    tool_type = tool_version.tool.tooltype.first()
    tool_type_localized_name = None

    language = translation.get_language()

    if tool_type:
        if language == 'fa':
            tool_type_localized_name = getattr(tool_type, 'name_fa')
        elif language == 'ar':
            tool_type_localized_name = getattr(tool_type, 'name_ar')
        else:
            tool_type_localized_name = getattr(tool_type, 'name')

    url = context.request.build_absolute_uri(
        pask_reverse(
            'webfrontend:toolversion',
            context.request,
            p_tool_id=tool_version.tool.id,
            p_platform_slug=tool_version.supported_os.slug_name,
        )
    )

    tool_logo_path = None
    if tool_logo:
        tool_logo_path = tool_logo.image.url

    default_image_path = settings.WEBFRONTEND_DEFAULT_IMAGE_PATH

    # =================================================
    # === Figure out if tool has extension versions ===
    # =================================================
    # extension_platforms = ['chrome', 'firefox']
    extensions_count = len([v for v in tool_versions if v.supported_os.category == 'w'])

    tool_has_extension_versions = True if extensions_count != 0 else False

    # ===========================================
    # === Figure out if tool has app versions ===
    # ===========================================
    tool_has_app_versions = False if len(tool_versions) == extensions_count else True

    return {
        'display_review_success': display_review_success,
        'display_support_success': display_support_success,
        'linux32_version': linux32_version,
        'windows32_version': windows32_version,
        'tool': tool,
        'tool_info': tool_info,
        'tool_logo_path': tool_logo_path,
        'tool_name_localized': tool_name_localized,
        'version_name_localized': version_name_localized,
        'tool_screenshots': tool_screenshots,
        'tool_version': tool_version,
        'tool_version_formatted_release_jdate':
            tool_version_formatted_release_jdate,
        'tool_version_has_guide': tool_version_has_guide,
        'version_blog_posts': version_blog_posts,
        'version_faqs': version_faqs,
        'version_tutorials': version_tutorials,
        'versiondownload_cache_placeholder': versiondownload_cache_placeholder,
        'versionrating_cache_placeholder': versionrating_cache_placeholder,
        'versionrating_count_cache_placeholder': versionrating_count_cache_placeholder,
        'version_rating': version_rating,
        'app': app,
        'no_version_rating_available': no_version_rating_available,
        'tool_versions': tool_versions,
        'tool_type_localized_name': tool_type_localized_name,
        'related_tools': related_tools,
        'url': url,
        'default_image_path': default_image_path,
        'tool_has_extension_versions': tool_has_extension_versions,
        'tool_has_app_versions': tool_has_app_versions,
    }
