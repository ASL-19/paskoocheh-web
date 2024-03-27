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


from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework import (
    viewsets,
    status,
)
from .models import (
    Text,
    ToolType,
)
from serializers import (
    TextSerializer,
    ToolTypeSeriaizer,
)


class TextViewSet(viewsets.GenericViewSet):
    """
        API ViewSet for Text model.
    """

    queryset = Text.objects.all()
    serializer_class = TextSerializer

    def list(self, request, *args, **kwargs):
        """
            List method to return response to GET requests for /

            Args:
            request: The request object from client
            *args, **kwargs: Extra arguments passed into the function

            Returns:
            Paginated response object containing the result of the request.
        """

        data = self.queryset

        serializer = self.get_serializer(
            data,
            many=True,
            context={'request': request})
        resp_data = serializer.data
        return Response(resp_data)

    def retrieve(self, request, version, pk=None):
        """
            Retrieve method to return response to GET request for a
            specific pk.

            Args:
            request: The request object from client
            version: The API version
            pk: The primary key of the object to return, the default is None.

            Returns:
            Response object containing the result of the request.
        """

        if version not in api_settings.ALLOWED_VERSIONS:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

        data = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(
            data,
            context={'request': request})
        resp_data = serializer.data
        return Response(resp_data)


class ToolTypeViewSet(viewsets.ModelViewSet):

    queryset = ToolType.objects.all()
    serializer_class = ToolTypeSeriaizer
