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


u"""statsweb URLs."""
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView
from rest_framework.routers import DefaultRouter
from stats.views import (
    ToolsTotalDownloadViewSet,
    TotalDownloadViewSet,
    DailyTotalDownloadViewSet,
    DailyTotalDownloadPerChannelViewSet,
    DailyTotalDownloadPerToolViewSet,
    DailyTotalDownloadPerPlatformViewSet,
    MonthlyTotalDownloadViewSet,
    MonthlyTotalDownloadPerChannelViewSet,
    MonthlyTotalDownloadPerToolViewSet,
    MonthlyTotalDownloadPerPlatformViewSet,
)

app_name = 'statsweb'

stats_api_router = DefaultRouter()
stats_api_router.register(
    r'stats/totaldownload',
    TotalDownloadViewSet
)
stats_api_router.register(
    r'stats/download',
    ToolsTotalDownloadViewSet,
    basename='download'
)
stats_api_router.register(
    r'stats/daily/download',
    DailyTotalDownloadViewSet,
    basename='daily_download'
)
stats_api_router.register(
    r'stats/daily/downloadperchannel',
    DailyTotalDownloadPerChannelViewSet,
    basename='daily_download_channel'
)
stats_api_router.register(
    r'stats/daily/downloadpertool',
    DailyTotalDownloadPerToolViewSet,
    basename='daily_download_tool'
)
stats_api_router.register(
    r'stats/daily/downloadperplatform',
    DailyTotalDownloadPerPlatformViewSet,
    basename='daily_download_platform'
)
stats_api_router.register(
    r'stats/monthly/download',
    MonthlyTotalDownloadViewSet,
    basename='monthly_download'
)
stats_api_router.register(
    r'stats/monthly/downloadperchannel',
    MonthlyTotalDownloadPerChannelViewSet,
    basename='monthly_download_channel'
)
stats_api_router.register(
    r'stats/monthly/downloadpertool',
    MonthlyTotalDownloadPerToolViewSet,
    basename='monthly_download_tool'
)
stats_api_router.register(
    r'stats/monthly/downloadperplatform',
    MonthlyTotalDownloadPerPlatformViewSet,
    basename='monthly_download_platform'
)

urlpatterns = (
    path(
        '',
        TemplateView.as_view(template_name="statsweb/index.html"),
        name='index',
    ),
    re_path(
        r'^api/(?P<version>(v1))/',
        include(stats_api_router.urls)
    ),
)
