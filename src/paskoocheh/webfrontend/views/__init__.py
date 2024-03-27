# coding: utf-8
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

"""Paskoocheh v3 front-end views."""

from .blogindex import BlogIndexView
from .blogpost import BlogPostView
from .blogposts import BlogPostsView
from .blogpostsfeed import BlogPostsFeedView
from .index import IndexView
from .pagenotfound import PageNotFoundView
from .page import PageView
from .search import SearchView
from .setandroidpromonoticehiddencookie import SetAndroidPromoNoticeHiddenCookieView
from .setplatform import SetPlatformView
from .tool import ToolView
from .toolfaq import ToolFaqView
from .toolfaqrecordclick import ToolFaqRecordClickView
from .toolfaqs import ToolFaqsView
from .toolversion import ToolVersionView
from .toolversiondownload import ToolVersionDownloadView
from .toolversionfaq import ToolVersionFaqView
from .toolversionfaqrecordclick import ToolVersionFaqRecordClickView
from .toolversionfaqs import ToolVersionFaqsView
from .toolversionguide import ToolVersionGuideView
from .toolversionrecordreferral import ToolVersionRecordReferralView
from .toolversionreview import ToolVersionReviewView
from .toolversionreviews import ToolVersionReviewsView
from .toolversiontutorial import ToolVersionTutorialView
from .toolversiontutorials import ToolVersionTutorialsView

# This is here to get PyFlakes to stop complaining about unused imports
__all__ = [
    "BlogIndexView",
    "BlogPostView",
    "BlogPostsView",
    "BlogPostsFeedView",
    "IndexView",
    "PageNotFoundView",
    "PageView",
    "SearchView",
    "SetAndroidPromoNoticeHiddenCookieView",
    "SetPlatformView",
    "ToolView",
    "ToolFaqView",
    "ToolFaqRecordClickView",
    "ToolFaqsView",
    "ToolVersionView",
    "ToolVersionDownloadView",
    "ToolVersionFaqView",
    "ToolVersionFaqRecordClickView",
    "ToolVersionFaqsView",
    "ToolVersionGuideView",
    "ToolVersionRecordReferralView",
    "ToolVersionReviewView",
    "ToolVersionReviewsView",
    "ToolVersionTutorialView",
    "ToolVersionTutorialsView",
]
