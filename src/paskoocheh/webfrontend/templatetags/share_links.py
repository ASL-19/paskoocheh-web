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

u"""Registers share_links Django template tag."""

import urllib.parse
from django import template
from webfrontend.utils.general import enforce_required_args
from django.conf import settings

register = template.Library()

app = settings.PLATFORM


@register.inclusion_tag('webfrontend/tags/share_links.html')
def share_links(
    url=None,
    title=None,
):
    u"""
    Build the context for the share_links inclusion tag.

    Required args:
        url(str)
        title(str): Localized title

    Returns:
        dictionary: Template context
    """
    enforce_required_args(
        locals(),
        'url',
        'title',
    )

    url_urlencoded = urllib.parse.quote_plus(url)

    twitter_text = None
    # This is assumed to be less than 280 characters, which should be more
    # than enough
    if app == 'zanga':
        twitter_text = '{title} {url} عن طریق @ZangaTech'.format(title=title, url=url)
    else:
        twitter_text = '{title} {url} از طریق @PasKoocheh'.format(title=title, url=url)

    twitter_text_urlencoded = urllib.parse.quote_plus(twitter_text)

    return {
        'app': app,
        'url_urlencoded': url_urlencoded,
        'twitter_text_urlencoded': twitter_text_urlencoded,
    }
