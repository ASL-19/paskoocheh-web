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

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from tools.models import HomeFeaturedTool, Tool, ToolType


class Command(BaseCommand):
    help = "Populates HomeFeaturedTool, Tool.primary_tooltype and Tool.slug"

    def handle(self, *args, **options):
        HomeFeaturedTool.objects.all().delete()
        HomeFeaturedTool.objects.create()

        for tool in Tool.objects.all():
            # Performing update() will skip save() and run faster
            Tool.objects.filter(pk=tool.pk).update(slug=slugify(tool.name))

        tool_type = ToolType.objects.create(name='Unknown', slug='unknown')
        Tool.objects.all().update(primary_tooltype=tool_type)
