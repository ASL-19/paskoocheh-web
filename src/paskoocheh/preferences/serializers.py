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
from .models import (
    Text,
    ToolType,
)


class ToolTypeSeriaizer(serializers.ModelSerializer):
    """
        Tool Type object
    """

    class Meta:

        model = ToolType
        read_only = True
        fields = (
            'id',
            'name',
            'icon',
        )


class TextSerializer(serializers.HyperlinkedModelSerializer):
    """
        Text object
    """

    language = serializers.SerializerMethodField()

    class Meta:

        model = Text
        read_only = True
        fields = (
            'id',
            'url',
            'language',
            'last_modified',
            'about',
            'contact_email',
            'privacy_policy',
            'terms_of_service')

    def get_language(self, obj):

        return str(obj.language)
