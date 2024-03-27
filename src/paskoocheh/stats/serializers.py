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


from rest_framework import serializers
from .models import VersionDownload


class DownloadSerializer(serializers.ModelSerializer):

    class Meta:
        model = VersionDownload
        fields = (
            'last_modified',
            'tool',
            'tool_name',
            'platform_name',
            'download_count')


class ToolsTotalDownloadSerializer(serializers.Serializer):

    tool_id = serializers.IntegerField()
    tool = serializers.CharField()
    count = serializers.IntegerField()


class DailyTotalDownloadSerializer(serializers.Serializer):

    date = serializers.DateField()
    count = serializers.IntegerField()


class DailyTotalDownloadPerChannelSerializer(serializers.Serializer):

    date = serializers.DateField()
    channel = serializers.CharField()
    count = serializers.IntegerField()


class DailyTotalDownloadPerToolSerializer(serializers.Serializer):

    date = serializers.DateField()
    tool_id = serializers.IntegerField()
    tool = serializers.CharField()
    count = serializers.IntegerField()


class DailyTotalDownloadPerPlatformSerializer(serializers.Serializer):

    date = serializers.DateField()
    platform = serializers.CharField()
    count = serializers.IntegerField()


class MonthlyTotalDownloadSerializer(serializers.Serializer):

    month = serializers.IntegerField()
    year = serializers.IntegerField()
    count = serializers.IntegerField()


class MonthlyTotalDownloadPerChannelSerializer(serializers.Serializer):

    month = serializers.IntegerField()
    year = serializers.IntegerField()
    channel = serializers.CharField()
    count = serializers.IntegerField()


class MonthlyTotalDownloadPerToolSerializer(serializers.Serializer):

    month = serializers.IntegerField()
    year = serializers.IntegerField()
    tool_id = serializers.IntegerField()
    tool = serializers.CharField()
    count = serializers.IntegerField()


class MonthlyTotalDownloadPerPlatformSerializer(serializers.Serializer):

    month = serializers.IntegerField()
    year = serializers.IntegerField()
    platform = serializers.CharField()
    count = serializers.IntegerField()
