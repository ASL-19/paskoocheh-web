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


from django.conf import settings
from paskoocheh.s3 import write_config_to_s3
from blog.models import (
    Post,
    Category,
)


def update_blog_json():
    """
        Update the review json configuration file
    """
    categories = Category \
        .objects \
        .all()

    categories_list = []
    for category in categories:
        categories_list.append({
            'id': category.id,
            'last_modified_date': category.last_modified_date.strftime('%Y-%m-%d %H:%M:%S'),
            'title': category.name,
            'content': category.name_ar,
            'tag': category.name_fa,
            'slug': category.slug,
            'logo': category.logo.url if category.logo else None,
            'description': category.description,
        })

    posts = Post \
        .objects \
        .filter(status='p') \
        .order_by('-published_date') \
        .all()

    posts_list = []
    for post in posts:
        posts_list.append({
            'id': post.id,
            'last_modified_date': post.last_modified_date.strftime('%Y-%m-%d %H:%M:%S'),
            'title': post.title,
            'content': post.content,
            'tags': post.tag_list,
            'category': post.category.name,
            'summary': post.summary,
            'slug': post.slug,
            'tool_tag': post.tool_tag_list,
            'version_tag': post.version_tag_list,
            'homepage_feature': post.homepage_feature,
            'feature_image': post.feature_image.url if post.feature_image else None,
            'feature_image_caption': post.feature_image_caption,
            'language': settings.LANGUAGE_SUPPORTED_DEFAULT
        })

    write_config_to_s3(
        {
            'categories': categories_list,
            'posts': posts_list
        },
        settings.S3_BLOG_POSTS_JSON
    )
