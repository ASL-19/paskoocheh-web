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


import boto3
import datetime
from django.conf import settings
import conffile.protobuf.schemas.python.paskoocheh_pb2 as paskoocheh
from tools.models import (
    Tool,
    Info,
    Image,
    VersionCode
)

PLATFORM_MAP = {
    "windows": {
        "name": paskoocheh.PlatformName.Value("WINDOWS"),
        "type": paskoocheh.PlatformType.Value("DESKTOP")
    },
    "ios": {
        "name": paskoocheh.PlatformName.Value("IOS"),
        "type": paskoocheh.PlatformType.Value("MOBILE")
    },
    "android": {
        "name": paskoocheh.PlatformName.Value("ANDROID"),
        "type": paskoocheh.PlatformType.Value("MOBILE")
    },
    "linux_32": {
        "name": paskoocheh.PlatformName.Value("LINUX_32"),
        "type": paskoocheh.PlatformType.Value("DESKTOP")
    },
    "linux_64": {
        "name": paskoocheh.PlatformName.Value("LINUX_64"),
        "type": paskoocheh.PlatformType.Value("DESKTOP")
    },
    "macos": {
        "name": paskoocheh.PlatformName.Value("MAC"),
        "type": paskoocheh.PlatformType.Value("DESKTOP")
    },
    "windows_phone": {
        "name": paskoocheh.PlatformName.Value("WINDOWSPHONE"),
        "type": paskoocheh.PlatformType.Value("MOBILE")
    },
    "firefox": {
        "name": paskoocheh.PlatformName.Value("FIREFOX"),
        "type": paskoocheh.PlatformType.Value("BROWSER")
    },
    "chrome": {
        "name": paskoocheh.PlatformName.Value("CHROME"),
        "type": paskoocheh.PlatformType.Value("BROWSER")
    },
    "ie": {
        "name": paskoocheh.PlatformName.Value("IE"),
        "type": paskoocheh.PlatformType.Value("BROWSER")
    },
    "opera": {
        "name": paskoocheh.PlatformName.Value("OPERA"),
        "type": paskoocheh.PlatformType.Value("BROWSER")
    }
}


def get_tools_for_platform(os_num, platform_type):
    """
        Get tools for given platform
    """

    tools = Tool.objects \
                .filter(publishable=True, versions__supported_os=os_num) \
                .prefetch_related('tooltype')

    return tools


class UTC(datetime.tzinfo):
    """
        UTC
    """

    ZERO = datetime.timedelta(0)

    def utcoffset(self, dt):
        return self.ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return self.ZERO


def totimestamp(dt, epoch=datetime.datetime(1970, 1, 1, 0, 0, 0, 0, UTC())):
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6


def get_latest_version_for_tool_os(tool, os):
    """
        Get latest version of tool
    """

    versions = tool.versions.all()
    latest = None
    if versions:
        for version in versions:
            if (version.supported_os.slug_name.lower() == paskoocheh.PlatformName.Name(os).lower()):
                if not latest:
                    latest = version
                elif version.release_date > latest.release_date:
                    latest = version
    return latest


def get_info_for_tool(tool):
    """
        Get Info for Tool record
    """

    return Info.objects.filter(tool=tool)


def get_logo_for_tool(tool):
    """
        Get Image for Tool record
    """

    # TODO: Image changes
    return Image.objects.filter(image_type="logo")


def get_screenshots_for_tool(tool):
    """
        Get Image for Tool record
    """

    # TODO: Image changes
    return Image.objects.filter(image_type="screenshot")


def write_pb_config_to_s3():  # noqa: C901
    """
        Output config from paskoocheh DB
    """

    tools = {}
    config_contents = paskoocheh.Config(bucket=settings.AWS_STORAGE_BUCKET_NAME,
                                        version=settings.S3_VERSION)
    for platform, value in PLATFORM_MAP.items():
        new_platform = config_contents.platforms.add()
        new_platform.name = value["name"]
        new_platform.type = value["type"]

        tools[platform] = get_tools_for_platform(value["name"], value["type"])
        for tool in tools[platform]:
            version = get_latest_version_for_tool_os(tool, value["name"])
            if version:
                version_code = VersionCode.objects.filter(version=version).first()
                if (version_code and version_code.s3_key and version_code.uploaded_file) or (version_code and version.download_url):
                    tool_infos = get_info_for_tool(tool)
                    tool_image = get_logo_for_tool(tool)
                    tool_screenshots = get_screenshots_for_tool(tool)

                    """ Tool Details """
                    new_tool = new_platform.tools.add()
                    new_tool.tool_id = tool.id
                    new_tool.is_opensource = tool.opensource
                    new_tool.is_recommended = tool.trusted
                    new_tool.is_featured = tool.featured
                    for ttype in tool.tooltype.all():
                        new_tool.tooltypes.append(ttype.id)
                    new_tool.contact.name = str(tool.name)
                    new_tool.contact.mail_responder_email = str(version.delivery_email)
                    new_tool.vendor.name = str(tool.name)
                    new_tool.vendor.website_url = str(tool.website)
                    new_tool.vendor.user_support_url = str(tool.contact_url)
                    new_tool.vendor.support_email = str(tool.contact_email)
                    new_tool.vendor.source_url = str(tool.source)
                    new_tool.vendor.facebook_url = str(tool.facebook)

                    """ Release Details """
                    for version_code in version.version_codes.all():
                        new_release = new_tool.releases.add()
                        new_release.version = str(version.version_number)
                        new_release.date_created = totimestamp(version.release_date)
                        new_release.date_released = totimestamp(version.release_date)
                        new_release.release_url = str(version_code.download_url)
                        if tool_image and tool_image[0] and tool_image[0].image:
                            new_release.icon = u"https://s3.amazonaws.com/" + settings.AWS_STORAGE_BUCKET_NAME + tool_image[0].image.url
                        if tool_screenshots:
                            for screenshot in tool_screenshots:
                                image_url = u"https://s3.amazonaws.com/" + settings.AWS_STORAGE_BUCKET_NAME + screenshot.image.url
                                new_release.screenshots.append(image_url)
                        new_release.binary.checksum = str(version_code.checksum)
                        new_release.binary.size = version_code.size
                        new_release.binary.path = str(version_code.s3_key)
                        new_release.package_name = str(version.package_name)
                        new_release.build_version = version_code.version_code

                    """ Translated Names """
                    for tool_info in tool_infos:
                        name = new_tool.contact.translation.add()
                        name.lang = str(tool_info.get_language_display())
                        name.name = str(tool_info.name)
                        name.description = str(tool_info.description)
                        vendor_name = new_tool.vendor.translation.add()
                        vendor_name.lang = str(tool_info.get_language_display())
                        vendor_name.name = str(tool_info.company)

    contents = config_contents.SerializeToString()
    s3_client = boto3.client("s3", region_name=settings.S3_REGION,
                             config=boto3.session.Config(signature_version="s3v4"))
    s3_client.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                         Key=settings.S3_CONFIG_PB,
                         Body=contents)
    return
