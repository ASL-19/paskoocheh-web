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


import conffile.protobuf.schemas.python.paskoocheh_pb2 as paskoocheh
from tools.models import (
    Image,
    Tutorial
)


class ConfigFile(paskoocheh.Config):
    """
        Config File model
    """

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
        "mac": {
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

    def __init__(self):
        """
            Init with bucket name and schema version
        """

        super(ConfigFile, self).__init__()

    def find_platform(self, operating_system):
        """
            Get platform definition for os
        """

        platform_name = self.PLATFORM_MAP[operating_system].name,
        platform_type = self.PLATFORM_MAP[operating_system].type

        platformlist = [platform for platform in self.platforms
                        if platform.name == platform_name]
        if len(platformlist) == 0:
            platform = self.platforms.add()
            platform.name = platform_name
            platform.type = platform_type
        else:
            platform = platformlist[0]

        return platform

    def find_tool(self, platform, tool_name):
        """
            Find tool for given platform and tool name (exact match)
        """

        toollist = [tool for tool in platform.tools if tool.contact.name == tool_name]
        if len(toollist) == 0:
            tool = self.platforms.tools.add()
        else:
            tool = toollist[0]

        return tool

    def _update_contact(self, tool, contact):
        """
            Update Tool Contact
        """

        tool.contact.website_url = contact.website
        tool.contact.user_support_url = contact.contact_url
        tool.contact.support_email = contact.contact_email
        tool.contact.blog_url = contact.blog
        tool.contact.facebook_url = contact.facebook
        tool.contact.twitter_handle = contact.twitter
        tool.contact.feed_url = contact.rss
        tool.contact.mail_responder_email = contact.delivery_email
        tool.contact.source_url = contact.source
        tool.contact.description = "Description for " + contact.name

    def _update_tool(self, tool, new_tool):
        """
            Update Tool
        """

        if tool.HasField("contact"):
            self._update_contact(tool, new_tool.contact)
        else:
            tool.contact = new_tool.name
            self._update_contact(tool, new_tool.contact)

        tool.type = new_tool.type
        tool.tags = [new_tool.type]
        tool.is_opensource = new_tool.opensource
        tool.is_recommended = False
        tool.is_featured = False
        # faqs = [faq for faq in Faq.objects.filter(tool=new_tool.id).all]
        # tool.vendor.add(contact)

    def find_release(self, tool, version):
        """
            Find release with exact version number
        """

        releases = [release for release in tool.releases
                    if release.version == version.version_number]
        if len(releases) == 0:
            version = tool.releases.add()
        else:
            version = releases[0]

    def update_release(self, release, version_code):
        """
            Update version for release
        """

        release.version = version_code.version.version_number
        if not release.HasField("date_created"):
            # TODO: Date Created has to be added to the model
            release.date_created = version_code.version.release_date
        release.rating = 0      # TODO
        release.download_count = version_code.version.download_count
        release.icon = ""       # TODO: Icon to be added
        release.date_modified = version_code.version.last_modified
        release.date_released = version_code.version.release_date
        release.release_url = version_code.version.release_url
        release.binary = self._create_binary(release, release.release_url)  # TODO
        # TODO release.screenshots are now tool screen shots
        if release.HasField("screenshots"):
            del release.screenshots
        # TOTO: Image changes
        images = Image.objects.filter(tool=version_code.version.tool.id).all
        for image in images:
            release.screenshots.append(image.url)
        # TODO release.tutorial needs language and OS
        if release.HasField("tutorials"):
            del release.tutorials
        tutorials = Tutorial.objects.filter(tool=version_code.version.tool.id).all
        for tutorial in tutorials:
            if tutorial.video:
                release.tutorials.append(tutorial.url)
            elif tutorial.youtube_link:
                release.tutorials.append(tutorial.youtube_link)
            else:
                release.tutorials.append(tutorial.vimeo_link)

        release.package_name = version_code.version.package_name
        release.build_version = version_code.version_code

    def _create_version(self, version_code):
        """
            Create version for tool/platform
        """

        platform = self._find_platform(version_code.version.supported_os)
        tool = self._find_tool(platform, version_code.version.tool.contact.name)
        self._update_tool(tool, version_code.version.tool)

        release = self._find_release(tool, version_code.version.version_number)

        self._update_release(release, version_code)
