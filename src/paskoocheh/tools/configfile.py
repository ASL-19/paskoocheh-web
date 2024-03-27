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
import re
import time
import logging
import html2text
import markdown
from urllib.parse import urlparse
from django.conf import settings
from django.db.models import Q
from django.db import connection
from paskoocheh.helpers import namedtuplefetchall
from paskoocheh.s3 import write_config_to_s3
from tools.models import (
    Info,
    Tool,
    Version,
    Tutorial,
    Guide,
    Faq,
    VersionCode,
)
from stats.models import VersionReview
from preferences.models import (
    Text
)
from pyskoocheh.telegraph import (
    telegraph_tame_text,
    telegraph_create_pages
)
from pyskoocheh.util import change_digits
from telegraph import Telegraph

logger = logging.getLogger(__name__)
app = settings.PLATFORM
language_code = 'ar' if app == 'zanga' else 'fa'


def get_tool_infos(internet_shutdown_filter=False):
    """
        Retrieve tools Info

        Returns:
        A dictionary containing all the Info content for tools
    """

    if not internet_shutdown_filter:
        infos = Info.objects.all()
    else:
        infos = Info.objects.filter(tool__tooltype__slug='internet-shutdown-ir')

    tool_info = {}
    for inf in infos:
        if inf.tool.name not in tool_info:
            # We should keep minimum en and ar/fa in translation
            tool_info[inf.tool.name] = {
                language_code: {},
                'en': {}
            }

        if inf.language not in tool_info[inf.tool.name]:
            tool_info[inf.tool.name][inf.language] = {}

        tool_info[inf.tool.name][inf.language] = {
            'last_modified': inf.last_modified.strftime('%Y-%m-%d %H:%M:%S'),
            'name': inf.name,
            'company': inf.company,
            'description': inf.description
        }

    return tool_info


def get_tools(tool_info, internet_shutdown_filter=False):
    """
        Retrieve tools

        Args:
        tool_info: Info content for the tools
        internet_shutdown_filter: Defaults to False

        Returns:
        A dictionary containing Tools information
    """
    if not internet_shutdown_filter:
        tools = Tool.objects.filter(publishable=True)
    else:
        tools = Tool.objects.filter(publishable=True, tooltype__slug='internet-shutdown-ir')

    alltools = {}

    for tool in tools:
        if tool.name not in alltools:
            alltools[tool.name] = {
                'name': tool.name,
                'id': tool.id,
                'trusted': tool.trusted,
                'opensource': tool.opensource,
                'source': tool.source,
                'website': tool.website,
                'facebook': tool.facebook,
                'twitter': tool.twitter,
                'rss': tool.rss,
                'blog': tool.blog,
                'contact_email': tool.contact_email,
                'contact_url': tool.contact_url,
                'featured': tool.featured,
                'info': {language_code: {}, 'en': {}} if tool.name not in tool_info else tool_info[tool.name],
            }
            alltools[tool.name]['images'] = {
                'logo': [],
                'screenshot': []
            }
            for img in tool.images.all():
                if img.image_type not in alltools[tool.name]['images']:
                    # We only store screenshots and logos
                    continue
                alltools[tool.name]['images'][img.image_type] \
                    .append({'url': img.image.url, 'full_bleed': img.should_display_full_bleed})

    return alltools


def get_version_guides():
    """
        Retrieve Guides for Version objects

        Returns:
        A dictionary containing Guides for Version objects
    """

    guides = Guide.objects.all()
    version_guides = {}
    for guide in guides:
        version_name = str(guide.version)
        if version_name not in version_guides:
            version_guides[version_name] = []

        version_guides[version_name].append({
            'id': guide.id,
            'language': guide.language,
            'last_modified': guide.last_modified.strftime('%Y-%m-%d %H:%M:%S'),
            'headline': guide.headline,
            'body': guide.body,
            'order': guide.order,
        })

    return version_guides


def get_version_tutorials():
    """
        Retrieve Tutorials for Version objects

        Returns:
        A dictionary containing Tutorials for Version objects
    """

    tutorials = Tutorial.objects.filter(publishable=True)
    version_tutorials = {}
    for tut in tutorials:
        version_name = str(tut.version)

        if version_name not in version_tutorials:
            version_tutorials[version_name] = []

        version_tutorials[version_name].append({
            'id': tut.id,
            'language': tut.language,
            'last_modified': tut.last_modified.strftime('%Y-%m-%d %H:%M:%S'),
            'video': None if not tut.video else tut.video.url,
            'video_link': tut.video_link,
            'title': tut.title,
            'order': tut.order
        })

    return version_tutorials


def get_version_faqs():
    """
        Retrieve FAQs for Version objects, concatenating the Version FAQ with
        Tool FAQ for that Version

        Returns:
        A dictionary containing FAQs for Version objects
    """

    version_faqs = {}

    faqs = Faq.objects \
        .exclude(version__isnull=False) \
        .prefetch_related('tool__versions')

    for faq in faqs:
        for ver in faq.tool.versions.all():
            version_name = str(ver)
            if version_name not in version_faqs:
                version_faqs[version_name] = []

        version_faqs[version_name].append({
            u'language': faq.language,
            u'question': faq.headline,
            u'answer': faq.body,
            u'order': faq.order,
        })

    faqs = Faq.objects.exclude(version__isnull=True)
    for faq in faqs:
        version_name = str(faq.version)
        if version_name not in version_faqs:
            version_faqs[version_name] = []

        version_faqs[version_name].append({
            u'language': faq.language,
            u'question': faq.headline,
            u'answer': faq.body,
            u'order': faq.order,
        })
        if faq.tool.name in version_faqs:
            version_faqs[version_name].extend(
                version_faqs[faq.tool.name])

    return version_faqs


def update_config_json(internet_shutdown_versions=None):    # noqa: C901
    """
        Updates the json configuration file
    """

    if internet_shutdown_versions:
        tool_info = get_tool_infos(internet_shutdown_filter=True)
        alltools = get_tools(tool_info, internet_shutdown_filter=True)
    else:
        tool_info = get_tool_infos()
        alltools = get_tools(tool_info)

    version_guides = get_version_guides()
    version_tutorials = get_version_tutorials()
    version_faqs = get_version_faqs()

    # TODO: temporary id numbers for os
    osind = 0
    os_new = {}

    if internet_shutdown_versions:
        tool_versions = internet_shutdown_versions
    else:
        tool_versions = Version.objects.select_related().prefetch_related().all()

    allcategories = {}
    results = {}
    faq_results = {}
    gnt_results = {}

    for ver in tool_versions:
        if not ver.tool.publishable:
            continue

        os = ver.supported_os
        if os.slug_name not in results:
            results[os.slug_name] = []
            faq_results[os.slug_name] = []
            gnt_results[os.slug_name] = []

        if os.slug_name not in os_new:
            os_new[os.slug_name] = {
                'id': str(osind),
                'name': os.name,
                'display_name': {
                    language_code: os.display_name_ar if language_code == 'ar' else os.display_name_fa,
                    'en': os.display_name.replace('_', ' ').capitalize()
                },
                'slug_name': os.slug_name,
            }
            osind += 1

        url = ver.download_url

        images = {}
        for img in ver.images.all():
            if img.image_type not in images:
                images[img.image_type] = []

            images[img.image_type].append({'url': img.image.url, 'full_bleed': img.should_display_full_bleed})

        version_name = str(ver)
        ver_cats = []
        for toolType in ver.tool.tooltype.all():
            if toolType.id not in allcategories:
                allcategories[toolType.id] = {}
                allcategories[toolType.id]['id'] = toolType.id
                allcategories[toolType.id]['name'] = {
                    'en': toolType.name,
                    'fa': toolType.name_fa,
                    'ar': toolType.name_ar,
                }
                allcategories[toolType.id]['icon'] = None if not toolType.icon else {'url': toolType.icon.url, 'full_bleed': False}
            ver_cats.append(str(toolType.id))

        tuts = None if version_name not in version_tutorials else version_tutorials[version_name]
        guides = None if version_name not in version_guides else version_guides[version_name]
        faqs = None if version_name not in version_faqs else version_faqs[version_name]

        default_download_dict = {
            's3': '',
            'url': url,
            'email': ver.delivery_email
        }

        version_dict = {
            'id': ver.id,
            'os_id': os_new[os.slug_name]['id'],
            'app_name': alltools[ver.tool.name]['name'],
            'tool_id': alltools[ver.tool.name]['id'],
            'categories': ver_cats,
            'last_modified': ver.last_modified.strftime('%Y-%m-%d %H:%M:%S'),
            'version_number': ver.version_number,
            'release_date': ver.release_date.strftime('%Y-%m-%d %H:%M:%S'),
            'release_jdate': ver.release_jdate,
            'release_url': ver.release_url,
            'package_name': ver.package_name,
            'permissions': ver.permissions,
            'images': images,
            'faq_url': ver.faq_url,
            'guide_url': ver.guide_url,
            'version_code': 0,
            'download_via': default_download_dict,
            's3_bucket': settings.AWS_STORAGE_BUCKET_NAME,
            's3_key': '',
            'checksum': '',
            'size': 0,
            'signature_file': '',
            'is_installable': True,
        }

        # preparing list of devices with version code specific info and list of version code info
        devices_data = []
        version_code_data = []

        # getting version codes for each tool/ version
        version_codes = VersionCode.objects.filter(version=ver)

        executed = False
        if ver.is_bundled_app:
            for version_code in version_codes:
                download_dict = {
                    's3': 'https://' + settings.AWS_S3_CUSTOM_DOMAIN + version_code.s3_key,
                    'url': url,
                    'email': ver.delivery_email
                }
                temp_version_code_dict = {
                    'version_code': version_code.version_code,
                    'download_via': download_dict,
                    's3_bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    's3_key': version_code.s3_key,
                    'checksum': version_code.checksum if version_code.checksum else '',
                    'size': version_code.size,
                    'signature_file': version_code.sig_file.url if version_code.sig_file else '',
                }
                version_code_data.append(temp_version_code_dict)

                # executed flag to run below block only once/for one version code object only
                if not executed and version_code.uploaded_file:
                    # non_installable_extensions = ['pdf', 'html']
                    extension = version_code.uploaded_file.name.split(
                        '.')[-1].lower()
                    if extension in settings.NON_INSTALLABLE_FILE_EXTENSIONS:
                        version_dict['is_installable'] = False
                        version_dict.update(temp_version_code_dict)
                    executed = True

                # fetching devices list associated with this version_code
                device_list = version_code.devices.all()
                for device in device_list:
                    if device.properties:
                        properties = json.loads(device.properties)
                        device_dict = {
                            'device': properties.get('build.device', None),
                            'version_code': version_code.version_code
                        }
                        devices_data.append(device_dict)

        elif version_codes:
            version_code = list(version_codes)[0]
            download_dict = {
                's3': 'https://' + settings.AWS_S3_CUSTOM_DOMAIN + version_code.s3_key,
                'url': url,
                'email': ver.delivery_email
            }
            version_dict['version_code'] = version_code.version_code
            version_dict['download_via'] = download_dict
            version_dict['s3_bucket'] = settings.AWS_STORAGE_BUCKET_NAME
            version_dict['s3_key'] = version_code.s3_key
            version_dict['checksum'] = version_code.checksum if version_code.checksum else ''
            version_dict['size'] = version_code.size
            version_dict['signature_file'] = version_code.sig_file.url if version_code.sig_file else ''
            if version_code.uploaded_file:
                # non_installable_extensions = ['pdf', 'html']
                extension = version_code.uploaded_file.name.split(
                    '.')[-1].lower()
                if extension in settings.NON_INSTALLABLE_FILE_EXTENSIONS:
                    version_dict['is_installable'] = False

        version_dict['version_codes'] = version_code_data if version_code_data else None
        version_dict['devices'] = devices_data if devices_data else None

        results[os.slug_name].append(version_dict)
        faq_results[os.slug_name].append({
            'id': ver.id,
            'os_id': os_new[os.slug_name]['id'],
            'app_name': alltools[ver.tool.name]['name'],
            'tool_id': alltools[ver.tool.name]['id'],
            'last_modified': ver.last_modified.strftime('%Y-%m-%d %H:%M:%S'),
            'faq': faqs,
            'faq_url': ver.faq_url,
        })
        gnt_results[os.slug_name].append({
            'id': ver.id,
            'os_id': os_new[os.slug_name]['id'],
            'app_name': alltools[ver.tool.name]['name'],
            'tool_id': alltools[ver.tool.name]['id'],
            'last_modified': ver.last_modified.strftime('%Y-%m-%d %H:%M:%S'),
            'tutorial': tuts,
            'guide': guides,
            'guide_url': ver.guide_url
        })

    if internet_shutdown_versions:
        S3_APPS_CONFIG_JSON = f'{settings.S3_INTERNET_SHUTDOWN_DIR}/{settings.S3_APPS_CONFIG_JSON}'
        S3_FAQ_CONFIG_JSON = f'{settings.S3_INTERNET_SHUTDOWN_DIR}/{settings.S3_FAQ_CONFIG_JSON}'
        S3_GNT_CONFIG_JSON = f'{settings.S3_INTERNET_SHUTDOWN_DIR}/{settings.S3_GNT_CONFIG_JSON}'
    else:
        S3_APPS_CONFIG_JSON = settings.S3_APPS_CONFIG_JSON
        S3_FAQ_CONFIG_JSON = settings.S3_FAQ_CONFIG_JSON
        S3_GNT_CONFIG_JSON = settings.S3_GNT_CONFIG_JSON

    write_config_to_s3(
        {
            'os_ids': [value for key, value in os_new.items()],
            'categories': [value for key, value in allcategories.items()],
            'tools': [value for key, value in alltools.items()],
            'versions': results
        },
        S3_APPS_CONFIG_JSON
    )

    write_config_to_s3(
        {
            'versions': faq_results
        },
        S3_FAQ_CONFIG_JSON
    )

    write_config_to_s3(
        {
            'versions': gnt_results
        },
        S3_GNT_CONFIG_JSON
    )


def get_footer(language):

    footer = Text.objects.get(language=language).telegraph_footer
    footer = html2text.html2text(markdown.markdown(footer, extensions=['extra', 'smarty'], output_format='html5'))
    footer = re.sub(r'(#|[*]{2,})', '', footer)
    return telegraph_tame_text(footer) or ""


def write_telegraph_html(objs, path, obj_anchor, footer_anchor, page_title, header, header_image, next_page, language):

    word_limit = 8500
    hyper_list_list = []

    footer = get_footer(language)

    page_no = 1
    ind_left = 0
    q_count = 0
    more = False
    done = False

    url_d = []
    cont_d = []
    fullpath = path

    while not done and objs:
        unicode_page_len = 0
        child = []

        if page_no > 1:
            fullpath = path + '-' + str(page_no)

        url_d.append(fullpath)

        for index in range(ind_left, len(objs)):
            obj = objs[index]
            body = html2text.html2text(markdown.markdown(obj.body, extensions=['extra', 'smarty'], output_format='html5'))
            body = re.sub(r'(#|[*]{2,})', '', body)
            headline = html2text.html2text(markdown.markdown(obj.headline, extensions=['extra', 'smarty'], output_format='html5'))

            if (unicode_page_len +
                    len(obj.headline) +
                    len(body) +
                    len("\n\n")) < word_limit:

                q_count += 1
                q_text = headline
                a_text = body
                unicode_page_len += len(q_text + a_text + "\n")

                hyper_list_list.append(
                    {
                        "tag": "a",
                        "attrs": {
                            "href": fullpath + "#" + obj_anchor + '-' + change_digits(str(q_count), language_code)
                        },
                        "children": [
                            change_digits(str(q_count), language_code) + '. ' + q_text + '\n\n'
                        ]
                    }
                )

                child.append({"tag": "h4", "children": [obj_anchor + ' ' + change_digits(str(q_count), language_code)]})
                child.append({"tag": "h4", "children": telegraph_tame_text(q_text)})
                child.append({"tag": "p", "children": telegraph_tame_text(a_text)})
                ind_left += 1
                more = False
            else:
                more = True
                page_no += 1
                break

        if not more:
            done = True

        else:
            # Next page link with place holder
            child.append(
                {
                    "tag": "a",
                    "attrs": {
                        "href": "http://example.com/"
                    },
                    "children": [next_page]
                })

        cont = [{
            "tag": "p",
            "attrs": {
                "align": "\"right\""
            },
            "children": [{
                "tag": "strong",
                "children": hyper_list_list
            }] + [{
                "tag": "strong",
                "children": [{
                    "tag": "a",
                    "attrs": {
                        "href": '#' + footer_anchor.replace(' ', '-')
                    },
                    "children": [
                        footer_anchor + '\n\n'
                    ]
                }]
            }] + child + [{
                "children": [{
                    "tag": "hr"
                }, {
                    "children": [
                        footer_anchor
                    ],
                    "tag": "h4"
                }],
                "tag": "p"
            }] + footer
        }]

        if header_image is not None:
            cont[0]["children"] = [{
                "tag": "img",
                "attrs": {
                    "src": header_image
                }
            }] + cont[0]["children"]

        fullpath = fullpath.replace('/', '')
        cont_d.append({
            "path": fullpath,
            "title": page_title,
            "content": cont,
            "header": header})

    return cont_d, url_d


def telegraph_add_next_page(sel, res_data, next_page):
    '''
        Adds 'next page' links to telegra.ph pages

        Args:
        res_data: a dictionary with recently modified urls stored with
        structure {'os1: {'app1': ['url1', 'url2', ...]}, ...}
        sel: Telegraph object created with secret access token
    '''

    if len(res_data) > 1:
        for i in range(len(res_data) - 1):
            path = re.sub(r'^/', '', res_data[i])
            path = re.sub(r'/$', '', path)
            path = path.split('/')[-1]
            if path and len(path) > 0:
                page = sel.get_page(path, return_content=True, return_html=False)
                content = page['content'][0]['children']
                for idx, ch in enumerate(content):
                    try:
                        tag = ch['tag']
                        children = ch['children']
                        href = ch['attrs']['href']
                    except Exception:
                        continue
                    if tag == 'a' and children == [next_page] and href == 'http://example.com/':
                        page['content'][0]['children'][idx]['attrs']['href'] = res_data[i + 1]
                        page = sel.edit_page(path, page['title'], content, page['author_name'], page['author_url'])
                        break


def update_faqs_telegraph(instanceid):
    """
        Updates the telegra.ph FAQ pages
    """

    language = language_code
    objname = 'FAQ'
    anchorname = 'QUESTION'

    try:
        faq = Faq.objects.get(pk=instanceid)
    except Exception as exc:
        logger.error('Error accessing FAQ object (pk={}) (error={})'.format(str(instanceid), str(exc)))
        return

    tool = faq.tool
    version = faq.version
    if version is not None:
        versions = [version]
    else:
        versions = Version.objects.filter(tool=tool)

    lang = {}
    with open('tools/lang.json', 'rb') as langfile:
        lang = json.loads(langfile.read())

    sel = Telegraph(settings.TELEGRAPH_TOKEN)

    footer_anchor = lang['SOCIALNET_TITLE'][language]
    obj_anchor = lang[anchorname][language]
    obj_name = lang[objname][language]
    author = lang['AUTHOR'][language]
    next_page = lang['NEXTPAGE'][language]

    url_dict = {}

    for version in versions:
        cont_dic_list = []
        app = version.tool
        os = version.supported_os
        url_dict[os] = {}
        url_dict[os][app.name] = []

        ques = Faq.objects.filter(Q(tool=version.tool), Q(version=None) | Q(version=version)).filter(language=language)
        ques.order_by("order")

        header_image = version.images.filter(image_type='header') or version.tool.images.filter(image_type='header')
        header_image = header_image.first().image.url if len(header_image) > 0 else None
        path = urlparse(version.faq_url).path

        title = obj_name + ' ' + version.tool.name + ' - ' + version.supported_os.display_name.replace('(', '').replace(')', '') + ' '
        header = version.tool.name + ' (' + version.supported_os.display_name + ') - ' + objname
        cont_dic_list, url_d = write_telegraph_html(ques, path, obj_anchor, footer_anchor, title, header, header_image, next_page, language)

        url = telegraph_create_pages(cont_dic_list, sel, author)
        if len(url) > 0:
            version.faq_url = url[0]
            version.save()
        url_dict[os][app.name] = url

        # In order to not flood the Telegraph server
        time.sleep(20)

    for os in url_dict:
        for app in url_dict[os]:
            telegraph_add_next_page(sel, url_dict[os][app], next_page)


def update_guides_telegraph(instanceid):
    """
        Updates the telegra.ph guide pages
    """

    language = language_code
    objname = 'GUIDE'
    anchorname = 'STEP'

    try:
        guide = Guide.objects.get(pk=instanceid)
    except Exception as exc:
        logger.error('Error accessing Guide object (pk={}) (error={})'.format(str(instanceid), str(exc)))
        return

    version = guide.version

    lang = {}
    with open('tools/lang.json', 'rb') as langfile:
        lang = json.loads(langfile.read())

    sel = Telegraph(settings.TELEGRAPH_TOKEN)

    footer_anchor = lang['SOCIALNET_TITLE'][language]
    obj_anchor = lang[anchorname][language]
    obj_name = lang[objname][language]
    author = lang['AUTHOR'][language]
    next_page = lang['NEXTPAGE'][language]

    url_dict = {}

    cont_dic_list = []
    url_dict = []

    steps = Guide.objects.filter(version=version, language=language)
    steps.order_by("order")

    header_image = version.images.filter(image_type='header') or version.tool.images.filter(image_type='header')
    header_image = header_image.first().image.url if len(header_image) > 0 else None
    path = urlparse(version.guide_url).path

    title = obj_name + ' ' + version.tool.name + ' - ' + version.supported_os.display_name.replace('(', '').replace(')', '') + ' '
    header = version.tool.name + ' (' + version.supported_os.display_name + ') - ' + objname
    cont_dic_list, url_dict = write_telegraph_html(steps, path, obj_anchor, footer_anchor, title, header, header_image, next_page, language)

    url = telegraph_create_pages(cont_dic_list, sel, author)
    if len(url) > 0:
        version.guide_url = url[0]
        version.save()

    telegraph_add_next_page(sel, url, next_page)


def update_review_json():
    """
        Update the review json configuration file
    """

    reviews = VersionReview \
        .objects \
        .filter(checked=True) \
        .order_by('-timestamp') \
        .all()[:settings.MAX_REVIEWS_TO_STORE_IN_JSON]

    revs = []
    for rev in reviews:
        if not rev.text or len(rev.text) <= 3:
            continue
        revs.append({
            'id': rev.id,
            'tool_name': rev.tool_name,
            'tool_id': rev.tool_id,
            'platform_name': rev.platform_name,
            'subject': rev.subject,
            'text': rev.text,
            'rating': float(rev.rating),
            'tool_version': rev.tool_version,
            'user_id': rev.user_id,
            'timestamp': rev.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'language': settings.LANGUAGE_SUPPORTED_DEFAULT
        })

    write_config_to_s3(
        revs,
        settings.S3_REVIEWS_CONFIG_JSON
    )


def update_download_rating_json():
    """
        Update the download and rating json configuration file
    """

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT "
            "   tool_name, vd.tool_id, platform_name, download_count, star_rating, rating_count "
            "FROM "
            "   stats_versiondownload vd "
            "FULL OUTER JOIN "
            "   stats_versionrating vr "
            "USING "
            "   (tool_name, platform_name) ")

        records = namedtuplefetchall(cursor)

    if len(records) == 0:
        return

    res = []
    for rec in records:
        if rec.tool_id:
            res.append({
                'tool_name': rec.tool_name,
                'tool_id': rec.tool_id,
                'platform_name': rec.platform_name,
                'download_count': rec.download_count if rec.download_count is not None else 0,
                'rating': float(rec.star_rating) if rec.star_rating is not None else None,
                'rating_count': rec.rating_count,
            })

    write_config_to_s3(
        res,
        settings.S3_DOWNLOAD_RATING_CONFIG_JSON,
    )
