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


from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import (
    DownloadSerializer,
    ToolsTotalDownloadSerializer,
    DailyTotalDownloadSerializer,
    DailyTotalDownloadPerChannelSerializer,
    DailyTotalDownloadPerToolSerializer,
    DailyTotalDownloadPerPlatformSerializer,
    MonthlyTotalDownloadSerializer,
    MonthlyTotalDownloadPerChannelSerializer,
    MonthlyTotalDownloadPerToolSerializer,
    MonthlyTotalDownloadPerPlatformSerializer,
)
from .models import VersionDownload
from .api_engine import (
    get_tools_total_download,
    get_daily_total_download,
    get_daily_total_download_per_channel,
    get_daily_total_download_per_tool,
    get_daily_total_download_per_platform,
    get_monthly_total_download,
    get_monthly_total_download_per_channel,
    get_monthly_total_download_per_tool,
    get_monthly_total_download_per_platform,
)


class TotalDownloadViewSet(viewsets.GenericViewSet):
    """
        Django view class for tools downloads
    """

    queryset = VersionDownload.objects.all()
    serializer_class = DownloadSerializer

    def list(self, request, *args, **kwargs):
        """
            List Tools
        """

        queryset = self.queryset
        serializer = self.get_serializer(
            queryset,
            context={'request': request},
            many=True)

        return Response(serializer.data)

    def retrieve(self, request, version, pk=None):
        """
            Get Version
        """

        if pk:
            queryset = self.queryset.filter(tool=pk).first()
            serializer = self.get_serializer(
                queryset,
                context={'request': request})

            return Response(serializer.data)


class ToolsTotalDownloadViewSet(viewsets.ViewSet):
    """
        Viewset class for total downloads for apps
    """

    serializer_class = ToolsTotalDownloadSerializer

    def list(self, request, version):
        """
            Return total download based in a period of time
        """

        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        data = get_tools_total_download(start, end)

        serializer = self.serializer_class(
            data,
            many=True)

        return Response(serializer.data)


class DailyTotalDownloadViewSet(viewsets.ViewSet):
    """
        Viewset class for daily total downloads for apps
    """

    serializer_class = DailyTotalDownloadSerializer

    def list(self, request, version):
        """
            Return total download based in a period of time
        """

        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        data = get_daily_total_download(start, end)

        serializer = self.serializer_class(
            data,
            many=True)

        return Response(serializer.data)


class DailyTotalDownloadPerChannelViewSet(viewsets.ViewSet):
    """
        Viewset class for daily total downloads for apps per channel
    """

    serializer_class = DailyTotalDownloadPerChannelSerializer

    def list(self, request, version):
        """
            Return total download based in a period of time
        """

        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        data = get_daily_total_download_per_channel(start, end)

        serializer = self.serializer_class(
            data,
            many=True)

        return Response(serializer.data)


class DailyTotalDownloadPerToolViewSet(viewsets.ViewSet):
    """
        Viewset class for daily total downloads for apps per tool
    """

    serializer_class = DailyTotalDownloadPerToolSerializer

    def list(self, request, version):
        """
            Return total download based in a period of time
        """

        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        data = get_daily_total_download_per_tool(start, end)

        serializer = self.serializer_class(
            data,
            many=True)

        return Response(serializer.data)


class DailyTotalDownloadPerPlatformViewSet(viewsets.ViewSet):
    """
        Viewset class for daily total downloads for apps per platform
    """

    serializer_class = DailyTotalDownloadPerPlatformSerializer

    def list(self, request, version):
        """
            Return total download based in a period of time
        """

        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        data = get_daily_total_download_per_platform(start, end)

        serializer = self.serializer_class(
            data,
            many=True)

        return Response(serializer.data)


class MonthlyTotalDownloadViewSet(viewsets.ViewSet):
    """
        Viewset class for monthly total downloads for apps
    """

    serializer_class = MonthlyTotalDownloadSerializer

    def list(self, request, version):
        """
            Return total download based in a period of time
        """

        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        data = get_monthly_total_download(start, end)

        serializer = self.serializer_class(
            data,
            many=True)

        return Response(serializer.data)


class MonthlyTotalDownloadPerChannelViewSet(viewsets.ViewSet):
    """
        Viewset class for monthly total downloads for apps per channel
    """

    serializer_class = MonthlyTotalDownloadPerChannelSerializer

    def list(self, request, version):
        """
            Return total download based in a period of time
        """

        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        data = get_monthly_total_download_per_channel(start, end)

        serializer = self.serializer_class(
            data,
            many=True)

        return Response(serializer.data)


class MonthlyTotalDownloadPerToolViewSet(viewsets.ViewSet):
    """
        Viewset class for monthly total downloads for apps per tool
    """

    serializer_class = MonthlyTotalDownloadPerToolSerializer

    def list(self, request, version):
        """
            Return total download based in a period of time
        """

        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        data = get_monthly_total_download_per_tool(start, end)

        serializer = self.serializer_class(
            data,
            many=True)

        return Response(serializer.data)


class MonthlyTotalDownloadPerPlatformViewSet(viewsets.ViewSet):
    """
        Viewset class for monthly total downloads for apps per platform
    """

    serializer_class = MonthlyTotalDownloadPerPlatformSerializer

    def list(self, request, version):
        """
            Return total download based in a period of time
        """

        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        data = get_monthly_total_download_per_platform(start, end)

        serializer = self.serializer_class(
            data,
            many=True)

        return Response(serializer.data)
