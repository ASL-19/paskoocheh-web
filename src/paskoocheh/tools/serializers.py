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


from boto3.session import Session
from botocore.client import Config
from botocore.exceptions import ClientError
from rest_framework import serializers
from django.conf import settings
from django.core.exceptions import FieldError
from tools.models import (
    Tool,
    Version,
    Info,
    # Report,
    Tutorial,
    Faq,
    Guide,
)
from preferences.serializers import ToolTypeSeriaizer


class ImageField(serializers.HyperlinkedRelatedField):
    """
        Customized field to represent the Image model for
        serialization.
    """

    def to_representation(self, value):
        """
            Overriding to_representation in order to put the type and
            url properties in a dictionary.

            Args:
            value: the object to be deserialized.

            Returns:
            A dictionary containing the type and the url to the ScreenShot
        """

        request = self.context.get('request')
        return {
            'type': value.image_type,
            'url': request.build_absolute_uri(value.image.url)
        }


class VersionSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Version
    """

    s3_temp_url = serializers.SerializerMethodField()
    images = ImageField(many=True, read_only=True, view_name='image-list')
    supported_os = serializers.StringRelatedField(read_only=True)

    class Meta:

        model = Version
        depth = 1
        fields = (
            'id',
            'last_modified',
            'supported_os',
            'images',
            'version_number',
            'download_url',
            'release_url',
            'release_date',
            'delivery_email',
            'tool',
            # 's3_temp_url'
        )

        read_only_fields = (
            'id',
            'last_modified',
            'supported_os',
            'version_number',
            'download_url',
            'release_url',
            'release_date',
            'delivery_email',
            'tool',
            # 's3_temp_url'
        )

    # TODO: Do we still need this? moved to webfrontend/utils/general.py
    def get_s3_temp_url(self, version):
        """
            Get s3 temp url using api credentials
        """

        if not version.s3_key:
            return ''
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
            settings.S3_REGION,
            config=s3_config)
        try:
            link = s3_client.generate_presigned_url(
                ExpiresIn=expiry,
                ClientMethod='get_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': version.s3_key.strip('/'),
                }
            )
        except ClientError as error:
            raise FieldError(f"Error generating s3 temp link for version: {str(error)}")
        return link

    def update(self, instance, validated_data):
        """
            Update download count
        """

        instance.save()
        return instance


class InfoSerializer(serializers.ModelSerializer):
    """
        Serialize Tool Info
    """

    class Meta:

        model = Info
        fields = (
            'id',
            'last_modified',
            'name',
            'description',
            'language',
            'company')


class TutorialSerializer(serializers.ModelSerializer):
    """
        Serialize Tutorial
    """

    class Meta:

        model = Tutorial
        depth = 1
        fields = (
            'id',
            'last_modified',
            'version',
            'language',
            'video',
            'video_link')


class FaqSerializer(serializers.ModelSerializer):
    """
        Serialize FAQ
    """

    class Meta:

        model = Faq
        depth = 1
        fields = (
            'id',
            'last_modified',
            'tool',
            'language',
            'headline',
            'body',
            'order')


class ToolSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Tool
    """

    versions = serializers.StringRelatedField(many=True, read_only=True)
    images = ImageField(many=True, read_only=True, view_name='image-list')
    infos = InfoSerializer(many=True, read_only=True)
    tooltype = ToolTypeSeriaizer(read_only=True, many=True)

    class Meta:

        model = Tool
        depth = 1
        fields = (
            'id',
            'last_modified',
            'url',
            'name',
            'last_update',
            'tooltype',
            'images',
            'versions',
            'opensource',
            'trusted',
            'infos',
            'featured')

        read_only_fields = (
            'id',
            'images')


class ToolDetailSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Tool Detail
        Using serializer for the versions because for detail we need more
        Remember you need to define related_name for each serializer in your model
    """

    versions = VersionSerializer(many=True, read_only=True)
    images = ImageField(many=True, read_only=True, view_name='image-list')
    infos = InfoSerializer(many=True, read_only=True)
    faqs = serializers.SerializerMethodField()
    tooltype = ToolTypeSeriaizer(read_only=True, many=True)

    class Meta:

        model = Tool
        depth = 1
        fields = (
            'id',
            'last_modified',
            'url',
            'name',
            'tooltype',
            'versions',
            'images',
            'faqs',
            'infos',
            'website',
            'facebook',
            'twitter',
            'rss',
            'blog',
            'contact_email',
            'contact_url',
            'opensource',
            'trusted',
            'featured')

    def get_faqs(self, tool):
        """
            Retrieve Tool Faq Info
        """

        qs = Faq.objects.filter(
            tool_id=tool.id,
            language=self.context.get('language_code'))
        faq_serializer = FaqSerializer(instance=qs, many=True)
        return faq_serializer.data


class GuideSerializer(serializers.ModelSerializer):
    """
        Serializer to handle Guide
    """

    class Meta:

        model = Guide
        depth = 1
        fields = (
            'id',
            'last_modified',
            'version',
            'language',
            'headline',
            'body',
            'order')

# class ReportSerializer(serializers.ModelSerializer):
#     tool = serializers.CharField(required=True, allow_blank=False)
#     email = serializers.EmailField(required=False, allow_blank=True)
#     reported_date = serializers.DateTimeField(required=False, allow_null=True)
#     country = serializers.CharField(max_length=64, required=True)
#     province = serializers.CharField(max_length=100, required=True)
#     city = serializers.CharField(max_length=100, required=False, allow_blank=True,
#                                  allow_null=True)
#     ISP = serializers.CharField(max_length=200, required=True)
#     speed = serializers.CharField(max_length=16, required=True)
#     quality = serializers.IntegerField(allow_null=False, required=True)
#     facebook_quality = serializers.IntegerField(allow_null=True, required=False)
#     youtube_quality = serializers.IntegerField(allow_null=True, required=False)
#     platform = serializers.CharField(max_length=100, allow_null=True, required=False)
#     antivirus = serializers.CharField(max_length=64, allow_null=True, required=False)
#     firewall = serializers.CharField(max_length=64, allow_null=True, required=False)
#     comment = serializers.CharField(allow_null=True, required=False)
#
#     class Meta:
#         model = Report
#
#     def get_validation_exclusions(self, *args, **kwargs):
#         exclusions = super(ReportSerializer, self).get_validation_exclusions(args, kwargs)
#         return exclusions
#
#     def create(self, validated_data):
#         return Report.objects.create(**validated_data)
