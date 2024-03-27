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

from django import forms
from django.contrib import admin
from rewards.models import (
    AdminRewardsRecord,
    EarningMethod,
    RedemptionMethod,
    UserRewardsRecord)


class AdminsRewardsRecordsForm(forms.ModelForm):
    """
    Custom Form to check user balance before redeeming points
    """
    def clean(self):
        # Custom validations for points field
        cleaned_data = super().clean()

        points = cleaned_data.get('points')
        user = cleaned_data.get('user')
        method_type = cleaned_data.get('method_type')
        if method_type == 'redeem':
            profile = user.profile
            if not profile.can_redeem_points(points):
                raise forms.ValidationError(f'Cannot redeem more than user balance ({user.profile.points_balance} points)')
        return cleaned_data


@admin.register(AdminRewardsRecord)
class AdminsRewardsRecordsAdmin(admin.ModelAdmin):
    """
        Admin Rewards records admin panel
    """

    form = AdminsRewardsRecordsForm

    list_display = (
        'user',
        'method_type',
        'points',
        'description',
        'admin',
        'created',
        'updated'
    )

    list_filter = (
        'method_type',
        'admin',
    )

    raw_id_fields = ['user']

    def has_change_permission(self, request, obj=None):
        # If allowed, it will complicate
        # redemption check against user balance
        return False


@admin.register(UserRewardsRecord)
class UserRewardsRecordAdmin(admin.ModelAdmin):
    """
        User Rewards records admin panel
    """
    list_display = (
        'user',
        'earning_method',
        'created',
        'updated',
    )
    ordering = (
        'user',
        'earning_method',
        'created',
        'updated',
    )
    list_filter = (
        'earning_method__earning_method',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(EarningMethod)
class EarningMethodAdmin(admin.ModelAdmin):
    """
        Earning methods admin panel
    """
    list_display = (
        'earning_method',
        'earning_points',
    )
    ordering = (
        'earning_method',
        'earning_points',
    )


@admin.register(RedemptionMethod)
class RedemptionMethodAdmin(admin.ModelAdmin):
    """
        Redemption methods admin panel
    """
    list_display = (
        'redemption_method_en',
        'redemption_method_fa',
        'redemption_points',
    )
    ordering = (
        'redemption_method_en',
        'redemption_method_fa',
        'redemption_points',
    )
