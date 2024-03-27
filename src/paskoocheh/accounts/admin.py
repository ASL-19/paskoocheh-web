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

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from gqlauth.models import UserStatus, RefreshToken
from accounts.models import UserProfile
from rewards.models import ReferralLink


User = get_user_model()


class UserStatusAdmin(admin.StackedInline):
    model = UserStatus

    fieldsets = [
        (None, {
            'fields': ('verified', 'archived', ),
        }),
    ]


class UserProfileAdmin(admin.StackedInline):
    model = UserProfile

    fieldsets = [
        (None, {
            'fields': ('pin', 'avatar', 'installed_apps', 'referred_by', ),
        }),
    ]

    fk_name = 'user'


class ReferralLinkAdmin(admin.StackedInline):
    """
        Referral links admin panel
    """
    model = ReferralLink
    fieldsets = [
        (None, {
            'fields': [('referral_slug', 'times_referred', )],
        }),
    ]
    readonly_fields = (
        'referral_slug',
        'times_referred',
    )

    def has_delete_permission(self, request, obj=None):
        return False


class CustomUserCreateForm(UserCreationForm):
    """
    Custom User creation form
    """

    class Meta(UserCreationForm.Meta):
        model = User


class CustomUserChangeForm(UserChangeForm):
    """
    Custom User change form
    """

    class Meta(UserChangeForm.Meta):
        model = User


class UserAdmin(UserAdmin):
    """
    Custom User admin panel
    """
    add_form = UserCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name',
                'last_name',
                'username',
                'email',
                'password1',
                'password2',
            ),
        }),
    )

    form = CustomUserChangeForm

    list_display = [
        'username',
        'email',
        'is_superuser',
        'verified',
        'points_balance',
    ]

    list_filter = UserAdmin.list_filter

    inlines = [
        UserStatusAdmin,
        UserProfileAdmin,
        ReferralLinkAdmin,
    ]

    @admin.display
    def points_balance(self, obj):
        return obj.profile.points_balance

    def verified(self, obj):
        return obj.status.verified
    verified.boolean = True
    verified.admin_order_field = 'status__verified'
    verified.short_description = 'Verified'

    # Only show the User status inline on the change form
    def get_inlines(self, request, obj=None):
        if obj:
            return [
                UserStatusAdmin,
                UserProfileAdmin,
                ReferralLinkAdmin,
            ]
        else:
            return []


admin.site.unregister(User)
admin.site.unregister(UserStatus)
admin.site.unregister(RefreshToken)
admin.site.register(User, UserAdmin)
