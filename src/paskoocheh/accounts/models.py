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

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum, F, Value

from paskoocheh.models import DatesMixin
from tools.models import Version, VersionCode
from rewards.models import (
    AdminRewardsRecord,
    UserRewardsRecord,
    EarningMethod)

User = get_user_model()


class InstalledApp(DatesMixin):
    """
    User Installed App definition (to track version updates)
    """
    app = models.ForeignKey(
        Version,
        related_name='installed_versions',
        verbose_name='Installed App',
        on_delete=models.CASCADE,
        blank=True)

    version_code = models.IntegerField(
        default=0)

    def __str__(self):
        return f'{self.version_code} | {str(self.app)}'


class UserProfile(DatesMixin):
    """
    User Profile definition
    """
    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE)

    pin = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(9999),
            MinValueValidator(1000)
        ],
        default=1234)

    referred_by = models.ForeignKey(
        User,
        related_name='referred_friend',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    avatar = models.ImageField(
        upload_to='profiles_avatars/',
        null=True,
        blank=True)

    installed_apps = models.ManyToManyField(
        InstalledApp,
        related_name='users',
        verbose_name='Associated Apps',
        blank=True)

    def __str__(self):
        return self.user.username

    @property
    def apps(self):
        """
            Returns a queryset of installed Versions
        """
        version_pks = list(self.installed_apps.values_list('app', flat=True))
        return Version.objects.filter(pk__in=version_pks).distinct()

    def install_or_update_app(self, version):
        """
            Adds new app to installed_apps
            Returns True if newly installed and False if installed/updated
        """
        version_code = 0

        version_codes = VersionCode.objects\
            .filter(version=version)\
            .order_by('-version_code')
        # This is the up-to-date app's version code
        if version_codes:
            version_code = version_codes[0].version_code

        installed_app, created = InstalledApp.objects.get_or_create(
            app=version,
            version_code=version_code)

        current_versions = self.installed_apps.filter(app=version)

        if not current_versions:
            # This is a new install
            self.installed_apps.add(installed_app)
            return True

        elif installed_app not in current_versions:
            # App is installed but not up-to-date
            # TODO: How do we handle this if the app was updated outside of Paskoocheh
            self.installed_apps.remove(*current_versions)
            self.installed_apps.add(installed_app)

            # This means this is an app update and user earns points
            self.earn_app_update()
            return False

        else:
            # installed_app in current versions
            # App is already installed
            return False

    @property
    def points_balance(self):
        """
            Calculates and returns user balance
        """

        admin_earnings = AdminRewardsRecord.objects\
            .filter(
                user=self.user,
                method_type='earn')\
            .aggregate(Sum('points'))['points__sum']
        admin_earnings = admin_earnings if admin_earnings else 0

        admin_redemptions = AdminRewardsRecord.objects\
            .filter(
                user=self.user,
                method_type='redeem')\
            .aggregate(Sum('points'))['points__sum']
        admin_redemptions = admin_redemptions if admin_redemptions else 0

        user_earnings = UserRewardsRecord.objects\
            .filter(user=self.user)\
            .aggregate(Sum('earning_method__earning_points'))['earning_method__earning_points__sum']
        user_earnings = user_earnings if user_earnings else 0

        user_balance = (user_earnings + admin_earnings) - admin_redemptions
        return user_balance

    def get_rewards_records(self):
        """
            Returns all user rewards records including admin records
            Args:
                self: UserProfile instance
            Returns:
                [RewardsRecordType]
        """

        all_records = []

        admin_earnings = AdminRewardsRecord.objects\
            .filter(
                user=self.user,
                method_type='earn')\
            .annotate(record_description=Value('admin_adjustment'))
        if admin_earnings:
            all_records.extend(list(admin_earnings))

        admin_redemptions = AdminRewardsRecord.objects\
            .filter(
                user=self.user,
                method_type='redeem')\
            .annotate(record_description=Value('admin_adjustment'))
        if admin_redemptions:
            all_records.extend(list(admin_redemptions))

        user_earnings = UserRewardsRecord.objects\
            .filter(user=self.user)\
            .annotate(method_type=Value('earn'))\
            .annotate(record_description=F('earning_method__earning_method'))\
            .annotate(points=F('earning_method__earning_points'))
        if user_earnings:
            all_records.extend(list(user_earnings))

        if all_records:
            all_records.sort(key=lambda x: x.updated, reverse=True)

        return all_records

    def can_redeem_points(self, points):
        """
            Checks redemption against user balance

            Args:
                self: UserProfile instance
                points: int, the number of points to redeem
            Returns:
                bool
        """

        user_balance = self.points_balance
        return points <= user_balance

    def earn_points(self, earning_method_name):
        """
            Creates a record of earning points

            Args:
                self: UserProfile instance
                earning_method: EarningMethod.earning_method
            Returns:
                UserRewardsRecord
        """

        earning_method = EarningMethod.objects.get(
            earning_method=earning_method_name)
        record = UserRewardsRecord.objects.create(
            user=self.user,
            earning_method=earning_method)
        return record

    def earn_quiz_completed(self):
        """
            Adds earning record for completing quiz
            Used in the reportQuizResults mutation
            Args:
                self: UserProfile instance
            Returns:
                UserRewardsRecord
        """
        return self.earn_points('quiz_completed')

    def earn_quiz_won(self):
        """
            Adds earning record for winning quiz
            Used in the reportQuizResults mutation
            Args:
                self: UserProfile instance
            Returns:
                UserRewardsRecord
        """
        return self.earn_points('quiz_won')

    def earn_referral(self):
        """
            Adds earning record for referrering / being referred
            Used in the verifyAccount mutation
            Args:
                self: UserProfile instance
            Returns:
                UserRewardsRecord
        """
        self.earn_points('referral')

    def earn_review(self):
        """
            Adds earning record for referrering / being referred
            Used in the writeReview mutation
            Args:
                self: UserProfile instance
            Returns:
                UserRewardsRecord
        """
        self.earn_points('review')

    def earn_app_update(self):
        """
            Adds earning record for updating installed app
            Used in the installOrUpdateApp mutation
            Args:
                self: UserProfile instance
            Returns:
                UserRewardsRecord
        """
        self.earn_points('update')
