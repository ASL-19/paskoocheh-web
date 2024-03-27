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

from unittest import skipIf

from django.conf import settings
from django.test import TestCase
from paskoocheh.schema import schema

from tools.models import Tool, ToolType, Version, VersionCode, HomeFeaturedTool
from stats.models import VersionDownload, VersionRating
from preferences.models import Platform


@skipIf(settings.BUILD_ENV != 'local', 'Disabled in CI')
class ToolAPITestCase(TestCase):
    """
    Testing tool app API
    """

    def setUp(self):
        self.maxDiff = None

        tool_dict = {
            'name': 'Tool',
            'slug': 'tool',
            'trusted': False,
            'featured': False,
            'opensource': False,
            'source': None,
            'website': 'https://play.google.com/store/apps/details?id=com.random.package',
            'facebook': None,
            'twitter': 'https://play.google.com/store/apps/details?id=com.random.package',
            'rss': None,
            'blog': 'https://play.google.com/store/apps/details?id=com.random.package',
            'contact_email': 'mail@example.com',
            'contact_url': 'https://play.google.com/store/apps/details?id=com.random.package',
            'publishable': True
        }
        version_dict = {
            'version_number': '000',
            'download_url': 'https://play.google.com/store/apps/details?id=com.random.package&hl=en',
            'release_url': None,
            'package_name': 'com.random.package',
            'auto_update': True,
            'permissions': 'android.permission.ACCESS_NETWORK_STATE,android.permission.INTERNET,android.permission.READ_EXTERNAL_STORAGE,android.permission.RECEIVE_BOOT_COMPLETED,android.permission.WAKE_LOCK,com.google.android.c2dm.permission.RECEIVE',
            'guide_url': '',
            'faq_url': '',
            'publishable': True,
            'video': '',
            'video_link': None,
            'is_bundled_app': True
        }
        verison_code_dict = {
            'version_code': 0,
            'uploaded_file': '',
            'checksum': None,
            'size': 0,
            'signature': None,
            'sig_file': ''
        }

        self.platform = Platform.objects.create(
            name='android',
            display_name_fa='android',
            slug_name='android',
            display_name='android')

        self.tool_type = ToolType.objects.create(slug='tool_type')
        self.tool_type_1 = ToolType.objects.create(slug='tool_type_1')
        tool_dict['primary_tooltype'] = self.tool_type_1
        self.tool = Tool.objects.create(**tool_dict)

        tool_dict['name'] = 'Tool 1'
        tool_dict['slug'] = 'tool1'
        tool_dict['primary_tooltype'] = self.tool_type
        tool_dict['website'] = 'https://play.google.com/store/apps/details?id=com.random.package1'
        self.tool_1 = Tool.objects.create(**tool_dict)

        tool_dict['name'] = 'Tool 2'
        tool_dict['slug'] = 'tool2'
        tool_dict['primary_tooltype'] = self.tool_type
        tool_dict['website'] = 'https://play.google.com/store/apps/details?id=com.random.package2'
        self.tool_2 = Tool.objects.create(**tool_dict)

        self.version = Version.objects.create(
            tool=self.tool,
            supported_os=self.platform,
            **version_dict)

        self.version_1 = Version.objects.create(
            tool=self.tool_1,
            supported_os=self.platform,
            **version_dict)

        self.version_2 = Version.objects.create(
            tool=self.tool_2,
            supported_os=self.platform,
            **version_dict)

        self.download = VersionDownload.objects.create(
            tool_name=self.tool.name,
            tool=self.tool,
            platform_name='android',
            download_count=100)

        self.download_1 = VersionDownload.objects.create(
            tool_name=self.tool_1.name,
            tool=self.tool_1,
            platform_name='android',
            download_count=50)

        self.download_2 = VersionDownload.objects.create(
            tool_name=self.tool_2.name,
            tool=self.tool_2,
            platform_name='android',
            download_count=200)

        self.rating = VersionRating.objects.create(
            tool_name=self.tool.name,
            tool=self.tool,
            platform_name='android',
            star_rating='2.0')

        self.rating_1 = VersionRating.objects.create(
            tool_name=self.tool_1.name,
            tool=self.tool_1,
            platform_name='android',
            star_rating='5.0')

        self.rating_2 = VersionRating.objects.create(
            tool_name=self.tool_2.name,
            tool=self.tool_2,
            platform_name='android',
            star_rating='4.3')

        self.version_code = VersionCode.objects.create(
            version=self.version,
            **verison_code_dict)

    def test_versions_query(self):
        versions_query = """
            query(
                $toolPk: Int,
                $platformSlug: String,
                $orderBy: [String],
            ){
                versions(
                    toolPk: $toolPk,
                    platformSlug: $platformSlug,
                    orderBy: $orderBy,
                ){
                    edges {
                        node {
                            tool {
                                name
                            }
                        }
                    }
                }
            }
            """
        response = schema.execute_sync(
            versions_query,
            variable_values={'toolPk': self.tool.pk})
        self.assertEqual(len(response.data['versions']['edges']), 1)

        response = schema.execute_sync(
            versions_query,
            variable_values={
                'platformSlug': 'android',
                'orderBy': '-download_count'})
        self.assertEqual(len(response.data['versions']['edges']), 3)
        self.assertEqual(
            response.data['versions']['edges'][0]['node']['tool']['name'],
            'Tool 2')
        self.assertEqual(
            response.data['versions']['edges'][1]['node']['tool']['name'],
            'Tool')
        self.assertEqual(
            response.data['versions']['edges'][2]['node']['tool']['name'],
            'Tool 1')

        response = schema.execute_sync(
            versions_query,
            variable_values={
                'platformSlug': 'android',
                'orderBy': '-star_rating'})
        self.assertEqual(len(response.data['versions']['edges']), 3)
        self.assertEqual(
            response.data['versions']['edges'][0]['node']['tool']['name'],
            'Tool 1')
        self.assertEqual(
            response.data['versions']['edges'][1]['node']['tool']['name'],
            'Tool 2')
        self.assertEqual(
            response.data['versions']['edges'][2]['node']['tool']['name'],
            'Tool')

        versions_with_category_argument_query = """
            query(
                $toolPk: Int,
                $platformSlug: String,
                $category: String,
                $orderBy: [String],
            ){
                versions(
                    toolPk: $toolPk,
                    platformSlug: $platformSlug,
                    category: $category,
                    orderBy: $orderBy,
                ){
                    edges {
                        node {
                            tool {
                                name
                            }
                        }
                    }
                }
            }
            """
        self.tool_1.tooltype.add(self.tool_type)
        self.tool_2.tooltype.add(self.tool_type)
        response = schema.execute_sync(
            versions_with_category_argument_query,
            variable_values={
                'category': 'tool_type',
                'platformSlug': 'android',
                'orderBy': '-star_rating'})
        self.assertEqual(len(response.data['versions']['edges']), 2)
        self.assertEqual(
            response.data['versions']['edges'][0]['node']['tool']['name'],
            'Tool 1')
        self.assertEqual(
            response.data['versions']['edges'][1]['node']['tool']['name'],
            'Tool 2')

    def test_tool_app(self):
        response = schema.execute_sync(
            """
            fragment CategoryAnalysis on CategoryAnalysisNode {
            rating
            ratingCategory{
                ...RatingCategory
            }
            }

            fragment Faq on FaqNode {
            clickCount
            video
            version {
                ...Version
            }
            tool{
                ...Tool
            }
            }

            fragment Guide on GuideNode {
            slug
            video
            id
            version {
                ...Version
            }
            }

            fragment Info on InfoNode {
            language
            name
            company
            description
            publishable
            tool {
                ...Tool
            }
            }

            fragment Platform on PlatformNode {
            name
            displayNameFa
            displayNameAr
            displayName
            slugName
            category
            icon
            }

            fragment RatingCategory on RatingCategoryNode {
            name
            nameFa
            nameAr
            slug
            }

            fragment TeamAnalysis on TeamAnalysisNode {
            review
            pros
            cons
            tool {
                ...Tool
            }
            categoryAnalysis {
                ...CategoryAnalysis
            }
            }

            fragment ToolImage on ToolImageNode {
            image
            imageType
            width
            height
            shouldDisplayFullBleed
            order
            publish
            language
                }

            fragment Tool on ToolNode {
            name
            trusted
            featured
            opensource
            source
            website
            facebook
            twitter
            rss
            blog
            contactEmail
            contactUrl
            publishable
            toolTypes {
                ...ToolType
            }
            images {
                ...ToolImage
            }
            }

            fragment ToolType on ToolTypeNode {
            name
            nameFa
            nameAr
            slug
            icon
            }

            fragment Tutorial on TutorialNode {
            language
            video
            videoLink
            title
                order
            publishable
            version {
                ...Version
            }
            }

            fragment Version on VersionNode {
            downloadCount
            averageRating {
            starRating
            }
            reviews {
                edges {
                    node {
                        subject
                        text
                    }
                }
            }
            versionNumber
            downloadUrl
            releaseUrl
            packageName
            autoUpdate
            permissions
            guideUrl
            faqUrl
            publishable
            video
            videoLink
            isBundledApp
            tool {
                ...Tool
            }
            platform {
                ...Platform
            }
            }

            query($pk: Int!)
            {
            tool(pk: $pk) {
                ...Tool
            }
            version(toolPk: $pk, platformSlug:"android") {
                ...Version
            }
            tools {
                edges {
                node {
                    ...Tool
                }
                }
            }
            versions {
                edges {
                node {
                    ...Version
                }
                }
            }
            faqs(toolPk: $pk) {
                edges {
                node {
                    ...Faq
                }
                }
            }
            guides(toolPk: $pk, platformSlug: "android") {
                edges {
                node {
                    ...Guide
                }
                }
            }
            tutorials(toolPk: $pk, platformSlug: "android") {
                edges {
                node {
                    ...Tutorial
                }
                }
            }
            info(toolPk: $pk) {
                edges {
                node {
                    ...Info
                }
                }
            }
            teamAnalysis(toolPk: $pk) {
                ...TeamAnalysis
            }
            }
            """, variable_values={'pk': self.tool.pk})

        self.assertEqual(response.data['faqs'], {
            'edges': [
            ]
        })
        self.assertEqual(response.data['guides'], {
            'edges': [
            ]
        })
        self.assertEqual(response.data['info'], {
            'edges': [
            ]
        })
        self.assertEqual(response.data['teamAnalysis'], None)
        self.assertEqual(response.data['tool'], {
            'blog': 'https://play.google.com/store/apps/details?id=com.random.package',
            'contactEmail': 'mail@example.com',
            'contactUrl': 'https://play.google.com/store/apps/details?id=com.random.package',
            'facebook': None,
            'featured': False,
            'images': [
            ],
            'name': 'Tool',
            'opensource': False,
            'publishable': True,
            'rss': None,
            'source': None,
            'toolTypes': [
            ],
            'trusted': False,
            'twitter': 'https://play.google.com/store/apps/details?id=com.random.package',
            'website': 'https://play.google.com/store/apps/details?id=com.random.package'
        })
        self.assertEqual(len(response.data['tools']['edges']), 3)
        self.assertEqual(response.data['tutorials'], {
            'edges': [
            ]
        })
        self.assertEqual(response.data['version'], {
            'downloadCount': 100,
            'averageRating': {
                'starRating': '2.0'
            },
            'reviews': {'edges': []},
            'autoUpdate': True,
            'downloadUrl': 'https://play.google.com/store/apps/details?id=com.random.package&hl=en',
            'faqUrl': '',
            'guideUrl': '',
            'isBundledApp': True,
            'packageName': 'com.random.package',
            'permissions': 'android.permission.ACCESS_NETWORK_STATE,android.permission.INTERNET,android.permission.READ_EXTERNAL_STORAGE,android.permission.RECEIVE_BOOT_COMPLETED,android.permission.WAKE_LOCK,com.google.android.c2dm.permission.RECEIVE',
            'platform': {
                'category': 'd',
                'displayName': 'android',
                'displayNameAr': None,
                'displayNameFa': 'android',
                'icon': None,
                'name': 'android',
                'slugName': 'android'
            },
            'publishable': True,
            'releaseUrl': None,
            'tool': response.data['tool'],
            'versionNumber': '000',
            'video': None,
            'videoLink': None
        })
        self.assertEqual(len(response.data['versions']['edges']), 3)

    def test_home_page_featured_tool_query(self):
        home_page_featured_tool_query = """
            {
                homePageFeaturedTool {
                    name
                }
            }
            """

        response = schema.execute_sync(home_page_featured_tool_query)
        self.assertEqual(response.data['homePageFeaturedTool'], None)

        HomeFeaturedTool.objects.create(tool=self.tool)
        response = schema.execute_sync(home_page_featured_tool_query)
        self.assertEqual(response.data['homePageFeaturedTool']['name'], 'Tool')

        HomeFeaturedTool.objects.update(tool=None)
        response = schema.execute_sync(home_page_featured_tool_query)
        self.assertEqual(response.data['homePageFeaturedTool'], None)
