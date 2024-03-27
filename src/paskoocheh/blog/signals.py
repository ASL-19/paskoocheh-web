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


from paskoocheh.helpers import disable_for_loaddata
from paskoocheh.tasks import enable_latest_cloudfront_state_invalidate_flag


@disable_for_loaddata
def blogs_changed(sender, instance, **kwargs):

    from blog.tasks import update_json_blog

    update_json_blog()
    enable_latest_cloudfront_state_invalidate_flag()
