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


import json
import logging
import re
import uuid
import hashlib
import time
from datetime import datetime
from dateutil import parser
from urllib.parse import unquote
from django.core.exceptions import FieldError
from django.db.models import Count
from django.db.models.functions.datetime import TruncDate
from django.utils.translation import gettext as _
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework import (
    viewsets,
    permissions,
    status,
)
from rest_framework.settings import api_settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from boto3.session import Session
from botocore.exceptions import ClientError
from botocore.client import Config
from tools.models import (
    Tool,
    # Report,
    Version,
    Tutorial,
    Guide,
    Faq,
    VersionCode,
)
from tools.serializers import (
    ToolSerializer,
    VersionSerializer,
    ToolDetailSerializer,
    TutorialSerializer,
    GuideSerializer,
    FaqSerializer,
    # ReportSerializer,
)

from preferences.models import AndroidDeviceProfile


logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def report_devices(request, version='v1'):
    """
        Reports devices with no version code for a specific tool
    """

    data = request.data
    if 'device' not in data:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        codename = data['device']

    device_properties = {
        'build.id': data['id'] if 'id' in data else '',
        'build.bootloader': data['bootloader'] if 'bootloader' in data else '',
        'build.brand': data['brand'] if 'brand' in data else '',
        'build.device': data['device'] if 'device' in data else '',
        'build.fingerprint': data['fingerprint'] if 'fingerprint' in data else '',
        'build.hardware': data['hardware'] if 'hardware' in data else '',
        'build.manufacturer': data['manufacturer'] if 'manufacturer' in data else '',
        'build.model': data['model'] if 'model' in data else '',
        'build.product': data['product'] if 'product' in data else '',
        'build.radio': data['radio'] if 'radio' in data else '',
        'build.version.sdk_int': data['version_sdk'] if 'version_sdk' in data else '',
        'build.version.release': data['version_release'] if 'version_release' in data else '',
    }

    device_profile, created = AndroidDeviceProfile.objects.get_or_create(codename=codename)
    if created:
        try:
            name = ' '.join([data['manufacturer'], data['model']])
            api_level = data['version_sdk']
            device_profile.name = f'{name} (api{api_level})'
            device_profile.properties = json.dumps(device_properties, indent=2, sort_keys=True)
            device_profile.status = 'ready'
            device_profile.save()
        except Exception as e:
            logger.error(f"Device: {codename} is missing some properties ({e}).")
            device_profile.name = codename
            device_profile.properties = json.dumps(device_properties, indent=2, sort_keys=True)
            device_profile.status = 'not_found'
            device_profile.save()

        logger.info(f"Added {codename} device successfully!")
        return Response(status=status.HTTP_201_CREATED)

    else:
        logger.info(f"Device: {codename} ({device_profile.name}) already exists.")
        return Response(status=status.HTTP_200_OK)


@permission_classes([permissions.IsAdminUser])
def delete_file_id(request, version='v1', version_id=None):    # noqa: C901
    """
        Deletes the file ID from Amazon S3 in order for the file to be uploaded
        again.

        This is needed in case something happen to the binary uploaded to telegram
        servers, and we want to upload the file again.
    """

    def delete_s3_key_fileid(s3_keys):
        """
            Deletes a file id from a given key list

            Args:
            key: S3 key list of the files to remove file id from <string>

            Return:
            True when successful for all the keys, False otherwise.
        """

        key_id = settings.AWS_ACCESS_KEY_ID
        secret_key = settings.AWS_SECRET_ACCESS_KEY
        session = Session(
            aws_access_key_id=key_id,
            aws_secret_access_key=secret_key
        )
        success = True
        for key in s3_keys:
            logger.info('Removing ID for {} {}'.format(settings.AWS_STORAGE_BUCKET_NAME, key))

            try:
                s3_config = Config(signature_version='s3v4')
                s3_client = session.client(
                    's3',
                    settings.S3_REGION,
                    config=s3_config)

                # We have to manually copy the ACL
                src_acl = s3_client.get_object_acl(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=key)
                new_acl = {
                    'Grants': src_acl['Grants'],
                    'Owner': src_acl['Owner'],
                }

                # And manually copy the metadata
                resp = s3_client.head_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=key)
                metadata = resp['Metadata']
                if settings.S3_METADATA_FILE_ID in metadata:
                    metadata.pop(settings.S3_METADATA_FILE_ID)

                s3_client.copy_object(
                    ACL='public-read-write',
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=key,
                    CopySource={
                        'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                        'Key': key
                    },
                    StorageClass='REDUCED_REDUNDANCY',
                    Metadata=metadata,
                    MetadataDirective='REPLACE')

                s3_client.put_object_acl(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=key,
                    AccessControlPolicy=new_acl)

            except ClientError as error:
                logger.error(
                    'ClientError deleting file ID "{}", Error: [{}]'.format(key, str(error)))
                success = False

        return success

    logger.info('delete_file_id called')

    url_name = 'admin:{}_{}_change'.format('tools', 'version')
    url = reverse(url_name, args=[version_id])

    if request.method != 'GET':
        return HttpResponseRedirect(url + '?del_status=400')

    if version_id is None or not Version.objects.filter(id=version_id):
        logger.warn('Missing Version ID/Version!')
        return HttpResponseRedirect(url)

    logger.info('Version ID is {}'.format(version_id))
    ver = Version.objects.filter(id=version_id).first()

    # Getting VersionCodes related with Version
    version_codes = ver.version_codes.all()
    if not version_codes:
        logger.info(
            'Version Code for Version ID {} does not exist!'.format(version_id))
        return HttpResponseRedirect(url)

    # Preparing list of s3 keys related with the version codes
    s3_keys = [vc.s3_key.strip('/') for vc in version_codes if vc.s3_key]
    if not s3_keys:
        logger.info(
            'No files/s3 keys are available for Version ID {}'.format(version_id))
        return HttpResponseRedirect(url)

    logger.info('files are {}'.format(s3_keys))
    if not delete_s3_key_fileid(s3_keys):
        logger.error(
            'Error deleting the file IDs for the Version ID: {}'.format(version_id))

    return HttpResponseRedirect(url)


def track_download(request, *args, **kwargs):
    """
        This is broken... it isn't defined as a proper rest-endpoint
        and if we do define it as an @api_view... it throws errors
        because of improper use of request.body
        If we try to have the function return a Response, it gives errors regarding
        use of Response() without a corresponding @api_view declaration
    """

    def action_log(user, action):
        if not user:
            user = uuid.uuid1()

        nowtime = time.time()
        table = 'action_log'
        source = 'PaskoochehWeb'
        user = hashlib.sha512(str(user)).hexdigest()
        key_id = settings.AWS_ACCESS_KEY_ID
        secret_key = settings.AWS_SECRET_ACCESS_KEY
        session = Session(
            aws_access_key_id=key_id,
            aws_secret_access_key=secret_key
        )

        try:
            s3_config = Config(
                signature_version='s3v4',
                s3={'addressing_style': 'path'})
            dynamodb = session.client(
                'dynamodb',
                settings.S3_REGION,
                config=s3_config)
            try:
                dynamodb.put_item(
                    TableName=table,
                    Item={
                        'user_name': {'S': str(user)},
                        'action_time': {'N': str(nowtime)},
                        'action_name': {'S': str(action)},
                        'source': {'S': str(source)},
                    })
            except ClientError as error:
                raise FieldError('Unable to retrieve action log: {}'.format(str(error)))
        except Exception as e:
            logger.error('Error writing to action log: {}'.format(str(e)))
            raise

    if request.method != "POST":
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if request.user.is_authenticated():
        user = request.user
    else:
        user = None

    req = json.loads(request.body)

    version_id = None
    if 'version_id' not in req:
        logger.warn('Track download function is called without passing any version_id to it')
        return JsonResponse(
            {
                'status': _('Failure'),
                'message': _('Bad request')
            },
            status=status.HTTP_400_BAD_REQUEST)

    version_id = req.get('version_id')
    version = Version.objects.get(pk=version_id)

    action = re.sub(r'\W+', '', version.tool.name.lower()) + '-' + re.sub(r'\W+', '', version.supported_os.slug_name.lower())
    action_log(user, action)
    return JsonResponse(
        {
            'status': _('Success')
        },
        status=status.HTTP_201_CREATED)


class VersionViewSet(viewsets.GenericViewSet):
    """
        Django view class for site versions
    """

    queryset = Version.objects.all()
    serializer_class = VersionSerializer

    def get_permissions(self):
        """
            Get Permissions for Tool View
        """

        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), )

    def list(self, request, *args, **kwargs):
        """
            List Tools
        """

        queryset = self.queryset
        queryset = queryset.filter(tool__publishable=True)
        language_cookie_value = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)

        if language_cookie_value:
            language_cookie_value = unquote(language_cookie_value).strip('\'')
            context = {
                'language_code': language_cookie_value,
                'request': request}
        else:
            context = {
                'language_code': settings.LANGUAGE_CODE,
                'request': request
            }

        serializer = self.serializer_class(queryset, context=context, many=True)
        return Response(serializer.data)

    def retrieve(self, request, version, pk=None):
        """
            Get Version
        """

        if pk:
            queryset = Version.objects.filter(id=pk, tool__publishable=True).first()
            language_cookie_value = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)

            if language_cookie_value:
                language_cookie_value = unquote(language_cookie_value).strip('\'')
                context = {
                    'language_code': language_cookie_value,
                    'request': request,
                }
            else:
                context = {
                    'language_code': settings.LANGUAGE_CODE,
                    'request': request,
                }

            serializer = self.serializer_class(queryset, context=context)
            return Response(serializer.data)


class ToolViewSet(viewsets.GenericViewSet):
    """
        Django view class for site toolset
    """

    queryset = Tool.objects.all()
    serializer_class = ToolSerializer

    def get_permissions(self):
        """
            Get Permissions for Tool View
        """

        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), )

    def list(self, request, *args, **kwargs):
        """
            List Tools
        """

        queryset = self.queryset
        queryset = queryset.filter(publishable=True)
        language_cookie_value = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)

        if language_cookie_value:
            language_cookie_value = unquote(language_cookie_value).strip('\'')
            context = {
                'language_code': language_cookie_value,
                'request': request}
        else:
            context = {
                'language_code': settings.LANGUAGE_CODE,
                'request': request
            }

        serializer = self.serializer_class(queryset, context=context, many=True)
        return Response(serializer.data)

    def retrieve(self, request, version, pk=None):
        """
            Get Tool
        """

        if pk:
            queryset = Tool.objects.filter(id=pk, publishable=True).first()
            language_cookie_value = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)

            if language_cookie_value:
                language_cookie_value = unquote(language_cookie_value).strip('\'')
                context = {
                    'language_code': language_cookie_value,
                    'request': request,
                }
            else:
                context = {
                    'language_code': settings.LANGUAGE_CODE,
                    'request': request,
                }

            serializer = ToolDetailSerializer(queryset, context=context)
            return Response(serializer.data)


@api_view(['GET'])
def version_link_view(request, version, version_id, version_code=0):
    queryset = Version.objects.filter(id=version_id)
    version = queryset[0]
    if not version:
        return Response({'error': 'No S3 link to wrap, Version not found'})

    vc = None
    # Android version code filtering
    if version.supported_os.slug_name == 'android':
        vc_queryset = VersionCode.objects.filter(
            version=version, version_code=version_code)
    else:
        vc_queryset = VersionCode.objects.filter(version=version)

    if not vc_queryset:
        return Response({'error': 'No S3 link to wrap, Version Code not found'})
    vc = vc_queryset.first()

    if not vc.s3_key:
        return Response({'error': 'No S3 link to wrap'})
    expiry = 600
    key_id = settings.AWS_ACCESS_KEY_ID
    secret_key = settings.AWS_SECRET_ACCESS_KEY
    session = Session(
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_key
    )
    s3_config = Config(
        signature_version='s3v4',
        s3={'addressing_style': 'path'})
    s3_client = session.client(
        's3',
        settings.S3_REGION, config=s3_config)
    try:
        link = s3_client.generate_presigned_url(
            ExpiresIn=expiry,
            ClientMethod='get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': vc.s3_key.strip('/'),
            }
        )
    except ClientError as error:
        raise FieldError('Error generating s3 temp link for version: {}'.format(str(error)))
    return Response({'link': link})


class VersionInstanceViewSet(viewsets.GenericViewSet):
    """
        The endpoint to take care of version referenced queries
    """

    def user_date_filter(self, data):
        """
            Filter to get query params for date range

                Args:
                data: QuerySet to apply filter too

                Returns:
                Filtered QuerySet based on QueryParams
        """

        try:
            fromdate = parser.parse(self.request.query_params.get('from', None))
            if fromdate:
                data = data.filter(
                    last_modified__gte=(datetime.date(fromdate)))
        except Exception:
            pass

        try:
            todate = parser.parse(self.request.query_params.get('to', None))
            if todate:
                data = data.filter(
                    last_modified__lte=(datetime.date(todate)))
        except Exception:
            pass

        return data

    def user_list_filter(self, data):
        """
            Filter the queryset based on users provided filters
            in query params
            This method is written specifically for list request

            Args:
            data: QuerySet to apply filter too

            Returns:
            Filtered QuerySet based on QueryParams
        """

        platform = self.request.query_params.get('os', None)
        if platform:
            data = data.filter(platform__iexact=platform)

        toolid = self.request.query_params.get('toolid', None)
        if toolid:
            data = data.filter(version__tool__id=toolid)

        verid = self.request.query_params.get('verid', None)
        if verid:
            data = data.filter(version__id=verid)

        vercode = self.request.query_params.get('vercode', None)
        if vercode:
            data = data.filter(version_code__iexact=vercode)

        lang = self.request.query_params.get('lang', None)
        if lang:
            data = data.filter(language=lang)

        data = self.user_date_filter(data)

        return data

    def user_retrieve_filter(self, data):
        """
            Filter the queryset based on users provided filters
            in query params
            This method is written specifically for retrieve request

            Args:
            data: QuerySet to apply filter too

            Returns:
            Filtered QuerySet based on QueryParams
        """

        channel = self.request.query_params.get('channel', None)
        if channel:
            data = data.filter(channel__iexact=channel)
            channel_version = self.request.query_params.get('channel_version', None)
            if channel_version:
                data = data.filter(channel_version=channel_version)

        data = self.user_date_filter(data)

        return data

    def list(self, request, *args, **kwargs):
        """
            List method to return response to GET requests for /

            It checks for 'q' parameters in query params for trigram search.

            Args:
            request: The request object from client
            *args, **kwargs: Extra arguments passed into the function

            Returns:
            Paginated response object containing the result of the request.
        """

        data = self.user_list_filter(self.queryset)
        if data.count() == 0:
            return Response([])

        all_values = [
            'tool_id',
            'tool_name',
            'version',
            'version_number',
            'version_code',
            'channel',
            'channel_version',
            'platform',
            'language',
            'date']

        groupby = self.request.query_params.get('groupby', None)
        if groupby:
            values = groupby.lower().split(',')
        else:
            values = all_values

        try:
            data = data.annotate(date=TruncDate('last_modified')) \
                .values(*values) \
                .annotate(count=Count('id'))
        except Exception:
            data = data.annotate(date=TruncDate('last_modified')) \
                .values(*all_values) \
                .annotate(count=Count('id'))

        return Response(data)

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

        data = self.queryset.filter(version__id=pk)
        if data.count() == 0:
            return Response([])

        data = self.user_retrieve_filter(data)
        if data.count() == 0:
            return Response([])

        first = data.first()

        resp_data = {
            'tool_id': first.tool_id,
            'tool_name': first.tool_name,
            'version': str(first.version),
            'version_number': first.version_number,
            'version_code': first.version_code,
            'platform': first.platform,
            'language': first.get_language_display()
        }

        all_values = [
            'channel',
            'channel_version',
            'date']

        groupby = self.request.query_params.get('groupby', None)
        if groupby:
            values = groupby.lower().split(',')
        else:
            values = all_values

        try:
            data = data.annotate(date=TruncDate('last_modified')) \
                .values(*values) \
                .annotate(count=Count('id'))
        except Exception:
            data = data.annotate(date=TruncDate('last_modified')) \
                .values(*all_values) \
                .annotate(count=Count('id'))

        resp_data['results'] = data

        return Response(resp_data)

    def create(self, request, version, *args, **kwargs):
        """
            Create method to return response to PUT request to
            create a record

            Args:
            request: The request object from client
            version: The API version

            Returns:
            Response object containing the result of the request.
        """

        if version not in api_settings.ALLOWED_VERSIONS:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
            Save the object

            Args:
            serializer: the serializer to use for saving the object
        """

        serializer.save()

    def get_success_headers(self, data):
        """
            Returns the headers for a Success create

            Args:
            data: The data to be passed back to he user
        """

        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}


class TutorialViewSet(viewsets.ReadOnlyModelViewSet):
    """
        The end point for tutorials
    """

    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer

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

        data = self.queryset.filter(version__id=pk)
        if data.count() == 0:
            return Response([])

        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
                context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            data,
            many=True,
            context={'request': request})
        resp_data = serializer.data
        return Response(resp_data)


class FaqViewSet(viewsets.ReadOnlyModelViewSet):
    """
        The end point for guides
    """

    queryset = Faq.objects.all()
    serializer_class = FaqSerializer

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

        data = self.queryset.filter(tool__id=pk)
        if data.count() == 0:
            return Response([])

        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
                context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            data,
            many=True,
            context={'request': request})
        resp_data = serializer.data
        return Response(resp_data)


class GuideViewSet(viewsets.ReadOnlyModelViewSet):
    """
        The end point for guides
    """

    queryset = Guide.objects.all()
    serializer_class = GuideSerializer

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

        data = self.queryset.filter(version__id=pk)
        if data.count() == 0:
            return Response([])

        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
                context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            data,
            many=True,
            context={'request': request})
        resp_data = serializer.data
        return Response(resp_data)


# class ReportView(generics.ListCreateAPIView): # pylint: disable=too-many-ancestors
#     queryset = Report.objects.all()
#     serializer_class = ReportSerializer
#
#     def get_permissions(self):
#         # check for permission of update and destroy
#         # If the HTTP method of the request ('GET', 'POST', etc) is 'safe', then
#         # anyone can use that endpoint. permissions are loaded either from
#         # permission.py or rest framework
#         if self.request.method in permissions.SAFE_METHODS:
#             return (permissions.AllowAny(),)
#
#         if self.request.method == 'POST':
#             return (permissions.AllowAny(),)
#
#         return (permissions.IsAuthenticated(),)
#
#     def list(self, request, *args, **kwargs): # pylint: disable=unused-argument
#         queryset = self.get_queryset()
#         serializer = ReportSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def create(self, request, *args, **kwargs): # pylint: disable=unused-argument
#         tool_id = request.POST.get('tool', None)
#
#         tool = Tool.objects.get(pk=tool_id)
#         serializer = self.serializer_class(data=request.data)
#
#         if serializer.is_valid(raise_exception=True):
#             agent = parse(request.META['HTTP_USER_AGENT'])
#             serializer.save(
#                 tool=tool,
#                 user_agent=request.META['HTTP_USER_AGENT'],
#                 user_agent_device_family=agent.browser.family,
#                 user_agent_os_family=agent.os.family,
#                 user_agent_os_version=agent.os.version,
#                 user_agent_browser_family=agent.browser.family,
#                 user_agent_browser_version=agent.browser.version,
#                 user_agent_is_mobile=agent.is_mobile,
#                 user_agent_is_tablet=agent.is_tablet,
#                 user_agent_is_touch=agent.is_touch_capable,
#                 user_agent_is_pc=agent.is_pc,
#                 user_agent_is_bot=agent.is_bot
#             )
#             # you can access to the data by serializer.data
#             return Response({
#                 'status': _('success'),
#                 'message': _('Report was submitted')
#             }, status=status.HTTP_201_CREATED)
#         else:
#             return Response({
#                 'status': _('Bad request'),
#                 'message': serializer.errors
#             }, status=status.HTTP_400_BAD_REQUEST)
# -*- coding: utf-8 -*-
# Paskoocheh - A tool marketplace for Iranian
