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

u"""webfrontend URLs."""

from django.urls import path, re_path
from django.views.generic.base import RedirectView
from webfrontend import views

app_name = 'webfrontend'
urlpatterns = (
    path(
        '',
        views.IndexView.as_view(),
        name='index'
    ),
    re_path(
        r'^blog\/$',
        views.BlogIndexView.as_view(),
        name='blogindex'
    ),
    re_path(
        r'^blog\/posts\/$',
        views.BlogPostsView.as_view(),
        name='blogposts'
    ),
    re_path(
        r'^blog\/posts\/index\.xml$',
        views.BlogPostsFeedView.as_view(),
        name='blogpostsfeed'
    ),
    re_path(
        r'^blog\/posts\/(?P<post_date>\d{4}-\d{2}-\d{2})-(?P<post_slug>[a-z-]+)\.html$',
        views.BlogPostView.as_view(),
        name='blogpost'
    ),
    path(
        'set-android-promo-notice-hidden-cookie',
        views.SetAndroidPromoNoticeHiddenCookieView.as_view(),
        name='setandroidpromonoticehiddencookie'
    ),
    path(
        'tools',
        RedirectView.as_view(
            url='%(path_prefix)s/tools/',
            permanent=True,
            query_string=True,
        )
    ),
    re_path(
        r'^tools\/$',
        views.SearchView.as_view(),
        name='search'
    ),
    path(
        'set-platform',
        views.SetPlatformView.as_view(),
        name='setplatform'
    ),
    re_path(
        r'^(?P<slug>(about|terms-of-service|privacy-policy|contact))\.html$',
        views.PageView.as_view(),
        name='page'
    ),
    # ToolView only exists to redirect to a ToolVersionView (or display an
    # error message if the tool_id has no version). There’s no concept of
    # viewing just a Tool. It will match “tools/1”, “tools/1.html”, or
    # “tools/1/”
    re_path(
        r'^tools\/(?P<tool_id>\d+)(\/|\.html)?$',
        views.ToolView.as_view()
    ),
    re_path(
        r'^tools/(?P<tool_id>\d+)/faqs/(?P<faq_id>\d+)\.html$',
        views.ToolFaqView.as_view(),
        name='toolfaq'
    ),
    re_path(
        r'^tools/(?P<tool_id>\d+)/faqs/(?P<faq_id>\d+)\/record-click$',
        views.ToolFaqRecordClickView.as_view(),
        name='toolfaqrecordclick'
    ),
    path(
        'tools/<int:tool_id>/faqs/',
        views.ToolFaqsView.as_view(),
        name='toolfaqs'
    ),
    re_path(
        r'^tools/(?P<tool_id>\d+)/(?P<platform_slug>\w+)\.html$',
        views.ToolVersionView.as_view(),
        name='toolversion'
    ),
    # Capture and redirect legacy “.html”-less toolversion URLs
    # e.g. /tools/19/ios -> /tools/19/ios.html
    re_path(
        r'^tools/(?P<tool_id>\d+)/(?P<platform_slug>\w+)\/?$',
        RedirectView.as_view(
            url='%(path_prefix)s/tools/%(tool_id)s/%(platform_slug)s.html',
            permanent=True,
        )
    ),
    re_path(
        r'^tools/(?P<tool_id>\d+)/(?P<platform_slug>\w+)/download$',
        views.ToolVersionDownloadView.as_view(),
        name='toolversiondownload'
    ),
    re_path(
        r'^tools/(?P<tool_id>\d+)/(?P<platform_slug>\w+)\/faqs\/(?P<faq_id>\d+)\.html$',
        views.ToolVersionFaqView.as_view(),
        name='toolversionfaq'
    ),
    re_path(
        r'^tools/(?P<tool_id>\d+)/(?P<platform_slug>\w+)\/faqs\/(?P<faq_id>\d+)\/record-click$',
        views.ToolVersionFaqRecordClickView.as_view(),
        name='toolversionfaqrecordclick'
    ),
    re_path(
        r'^tools/(?P<tool_id>\d+)/(?P<platform_slug>\w+)\/faqs\/$',
        views.ToolVersionFaqsView.as_view(),
        name='toolversionfaqs'
    ),
    re_path(
        r'^tools/(?P<tool_id>\d+)/(?P<platform_slug>\w+)\/guide\.html$',
        views.ToolVersionGuideView.as_view(),
        name='toolversionguide'
    ),
    re_path(
        r'^tools/(?P<tool_id>\d+)/(?P<platform_slug>\w+)\/tutorials\/(?P<tutorial_id>\d+)\.html$',
        views.ToolVersionTutorialView.as_view(),
        name='toolversiontutorial'
    ),
    re_path(
        r'^tools/(?P<tool_id>\d+)/(?P<platform_slug>\w+)\/tutorials\/$',
        views.ToolVersionTutorialsView.as_view(),
        name='toolversiontutorials'
    ),
    re_path(
        r'^tools/(?P<tool_id>\d+)/(?P<platform_slug>\w+)\/record-referral$',
        views.ToolVersionRecordReferralView.as_view(),
        name='toolversionrecordreferral'
    ),
    re_path(
        r'^tools/(?P<tool_id>\d+)/(?P<platform_slug>\w+)\/reviews\/(?P<review_id>\d+)\.html$',
        views.ToolVersionReviewView.as_view(),
        name='toolversionreview'
    ),
    re_path(
        r'^tools/(?P<tool_id>\d+)/(?P<platform_slug>\w+)\/reviews\/$',
        views.ToolVersionReviewsView.as_view(),
        name='toolversionreviews'
    ),
    re_path(
        r'',
        views.PageNotFoundView.as_view(),
        name='pagenotfound'
    ),
)
