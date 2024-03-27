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

import magic
import random
import secrets
import string
from uuid import UUID

from dataclasses import asdict

import strawberry
import strawberry_django
from strawberry.file_uploads.scalars import Upload

from django.contrib.auth import get_user_model
from django.core.signing import BadSignature, SignatureExpired
from django.utils import translation

from typing import Optional, List, Annotated

from gqlauth.core.constants import Messages
from gqlauth.core.exceptions import (
    TokenScopeError,
    UserAlreadyVerified,
)
from gqlauth.core.mixins import ArgMixin
from gqlauth.core.types_ import MutationNormalOutput
from gqlauth.core.utils import get_user, inject_fields, get_payload_from_token
from gqlauth.models import UserStatus
from gqlauth.settings import gqlauth_settings as app_settings
from gqlauth.user import arg_mutations as mutations
from gqlauth.user import resolvers
from gqlauth.user.queries import UserQueries

from paskoocheh.utils import (
    Connection,
    IsAuthenticatedField,
    IsAuthenticatedConnection)

from accounts.forms import UpdateAvatarForm
from accounts.models import UserProfile
from rewards.models import ReferralLink, QuizPage, QuizResult
from stats.models import VersionReview


User = get_user_model()
RewardsRecordType = Annotated['RewardsRecordType', strawberry.lazy('rewards.schema')]


@strawberry_django.type(User, pagination=True)
class MinimalUserNode(strawberry.relay.Node):
    """
    Relay: Minmal User Node
    """
    id: strawberry.relay.NodeID[int]
    username: str
    email: str

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        return queryset.select_related('status')

    @strawberry.field(extensions=[IsAuthenticatedField()])
    def purchased_apps(
        self,
        reviewed: Optional[bool] = strawberry.UNSET
    ) -> Optional[List[Optional[Annotated['VersionNode', strawberry.lazy('tools.schema')]]]]:
        try:
            profile = UserProfile.objects.get(user=self)
            apps = profile.apps.all()
            reviewed_apps = unreviewed_apps = []
            if reviewed is strawberry.UNSET:
                return apps
            elif reviewed and reviewed is not strawberry.UNSET:
                for app in apps:
                    if VersionReview.objects.filter(pask_user=self, tool=app.tool).exists():
                        reviewed_apps.append(app)
                return reviewed_apps
            elif not reviewed:
                for app in apps:
                    if not VersionReview.objects.filter(pask_user=self, tool=app.tool).exists():
                        unreviewed_apps.append(app)
                return unreviewed_apps
            else:
                return []
        except UserProfile.DoesNotExist:
            return []

    @strawberry.field(extensions=[IsAuthenticatedField()])
    def pin(self) -> int:
        try:
            profile = UserProfile.objects.get(user=self)
            return profile.pin
        except UserProfile.DoesNotExist:
            return 0

    @strawberry.field(extensions=[IsAuthenticatedField()])
    def points_balance(self) -> int:
        try:
            profile = UserProfile.objects.get(user=self)
            return profile.points_balance
        except UserProfile.DoesNotExist:
            return 0

    @strawberry.field(extensions=[IsAuthenticatedConnection()])
    def rewards_records(
        self,
        info: strawberry.types.Info,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Optional[Connection[RewardsRecordType]]:
        try:
            profile = UserProfile.objects.get(user=self)
            records = profile.get_rewards_records()
        except UserProfile.DoesNotExist:
            records = []
        return Connection[RewardsRecordType].resolve_connection(
            info=info,
            nodes=records,
            offset=offset,
            first=first,
            last=last,
            after=after,
            before=before)

    @strawberry.field(extensions=[IsAuthenticatedField()])
    def referral_slug(self) -> Optional[str]:
        try:
            referral_link = ReferralLink.objects.get(user=self)
            return referral_link.referral_slug
        except ReferralLink.DoesNotExist:
            return None

    @strawberry.field(extensions=[IsAuthenticatedField()])
    def has_finished_quiz(self, quiz_pk: int) -> bool:
        try:
            QuizResult.objects.get(
                user=self,
                quiz_id=quiz_pk)
        except QuizPage.DoesNotExist:
            return False
        except QuizResult.DoesNotExist:
            return False
        return True


@strawberry.type
class UserQuery(UserQueries):
    """
    User Queries
    """

    @strawberry.field(extensions=[IsAuthenticatedField()])
    def me(self, info: strawberry.types.Info) -> Optional[MinimalUserNode]:
        user = get_user(info)
        if not user.is_authenticated:
            return None
        return user  # type: ignore


class Register(mutations.Register):
    """
    Custom `Register` mutation
    """

    __doc__ = resolvers.RegisterMixin.__doc__

    @strawberry.input
    @inject_fields(app_settings.REGISTER_MUTATION_FIELDS)
    class RegisterInput:
        referral_slug: Optional[str] = None
        if not app_settings.ALLOW_PASSWORDLESS_REGISTRATION:
            password1: str
            password2: str

        if app_settings.REGISTER_REQUIRE_CAPTCHA:
            identifier: UUID
            userEntry: str

    @classmethod
    def resolve_mutation(cls, info, input_: RegisterInput) -> MutationNormalOutput:  # noqa C901 
        # Activate translations
        # for the activation email
        lang_code = translation.get_language()
        if lang_code:
            translation.activate(lang_code)

        # Convert email to lowercase and make sure it's unique
        input_.email = input_.email.lower()
        if User.objects.filter(email=input_.email).exists():
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        'message': 'User with that email already exists',
                        'code': 'unique'
                    }
                ]
            )

        output = super(Register, cls).resolve_mutation(info, input_)
        if output.errors:
            return output

        try:
            user = User.objects.get(
                email=input_.email,
                username=input_.username)
            user.full_clean()
            user.save()
        except User.DoesNotExist:
            translation.deactivate()
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        'message': 'User does not exist',
                        'code': 'user_not_created'
                    }
                ]
            )

        try:
            # Add user profile details
            profile = UserProfile.objects.create(
                user=user,
                pin=random.randint(1000, 9999))
            if input_.referral_slug:
                try:
                    referral = ReferralLink.objects.get(referral_slug=input_.referral_slug)
                    profile.referred_by = referral.user
                except ReferralLink.DoesNotExist:
                    pass
            profile.full_clean()
            profile.save()

        except Exception:
            translation.deactivate()
            user.delete()
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        'message': 'Could not create a profile for the user\
                            , check the parameters',
                        'code': 'profile'
                    }
                ]
            )

        try:
            # Create user referral link
            link_slug = ''.join(
                secrets.choice(
                    string.ascii_lowercase + string.digits) for _ in range(64))
            referral_link = ReferralLink.objects.create(
                user=user,
                referral_slug=link_slug)
            referral_link.save()

        except Exception:
            translation.deactivate()
            user.delete()
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        'message': 'Failed to generate referral link for user',
                        'code': 'referral_link'
                    }
                ]
            )

        # Deactivate translations
        if lang_code:
            translation.deactivate()

        return output


class SendPasswordResetEmail(mutations.SendPasswordResetEmail):
    """
    Custom `SendPasswordResetEmail` mutation
    """

    __doc__ = resolvers.SendPasswordResetEmailMixin.__doc__

    @classmethod
    def resolve_mutation(
        cls,
        info,
        input_: resolvers.SendPasswordResetEmailMixin.SendPasswordResetEmailInput
    ) -> MutationNormalOutput:

        # Activate translations
        # for the password reset email
        lang_code = translation.get_language()
        if lang_code:
            translation.activate(lang_code)

        output = super(SendPasswordResetEmail, cls).resolve_mutation(info, input_)

        # Deactivate translations
        if lang_code:
            translation.deactivate()

        return output


class DeleteAccount(mutations.DeleteAccount):
    """
    Custom `DeleteAccount` mutation
    """

    __doc__ = resolvers.DeleteAccountMixin.__doc__

    @classmethod
    def resolve_mutation(
        cls,
        info,
        input_: resolvers.DeleteAccountMixin.ArchiveOrDeleteMixinInput
    ) -> MutationNormalOutput:

        # Activate translations
        # for the password reset email
        lang_code = translation.get_language()
        if lang_code:
            translation.activate(lang_code)

        try:
            user = info.context.request.user
            UserProfile.objects.get(user=user).delete()
        except UserProfile.DoesNotExist:
            if lang_code:
                translation.deactivate()
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        'message': 'Failed to find profile for user',
                        'code': 'profile_not_found'
                    }
                ]
            )

        output = super(DeleteAccount, cls).resolve_mutation(info, input_)

        # Deactivate translations
        if lang_code:
            translation.deactivate()

        return output


class VerifyAccount(mutations.VerifyAccount):
    """
    Custom `VerifyAccount` mutation
    """

    __doc__ = resolvers.VerifyAccountMixin.__doc__

    @classmethod
    def resolve_mutation(
        cls,
        info,
        input_: resolvers.VerifyAccountMixin.VerifyAccountInput
    ) -> MutationNormalOutput:

        # Activate translations
        # for the password reset email
        lang_code = translation.get_language()
        if lang_code:
            translation.activate(lang_code)

        try:
            username = get_payload_from_token(input_.token, 'activation')['username']
            user = User.objects.get(username=username)

            UserStatus.verify(input_.token)

            user_profile = UserProfile.objects.get(user=user)
            friend = user_profile.referred_by
            if friend:
                friend_profile = friend.profile
                # Give both users their points once verification is done
                user_profile.earn_referral()
                friend_profile.earn_referral()

                # Update ReferralLink model for friend
                referral_link = ReferralLink.objects.get(user=friend)
                referral_link.times_referred += 1
                referral_link.save()
        except UserAlreadyVerified:
            return MutationNormalOutput(
                success=False,
                errors=Messages.ALREADY_VERIFIED)
        except SignatureExpired:
            return MutationNormalOutput(
                success=False,
                errors=Messages.EXPIRED_TOKEN)
        except (BadSignature, TokenScopeError):
            return MutationNormalOutput(
                success=False,
                errors=Messages.INVALID_TOKEN)

        if lang_code:
            translation.deactivate()

        return MutationNormalOutput(success=True)


class UpdateAvatar(MutationNormalOutput, ArgMixin):
    """
    Mutation to update user avatar
    """

    form = UpdateAvatarForm

    @strawberry.input
    class UpdateAvatarinput:
        avatar: Optional[Upload] = strawberry.UNSET

    @classmethod
    def resolve_mutation(cls, info, input_: UpdateAvatarinput) -> MutationNormalOutput:
        request = info.context.request
        user = request.user
        if user and user.is_authenticated:
            try:
                # Image file validation
                mime_type = magic.from_buffer(input_.avatar.read(2048), mime=True)
                if not mime_type.startswith('image'):
                    error_message = f'Failed to update avatar of user: {user} (check file format)'
                    error_code = 'file_not_allowed'
                    return MutationNormalOutput(
                        success=False,
                        errors=[
                            {
                                "message": error_message,
                                "code": error_code
                            }
                        ]
                    )

                f = cls.form(
                    asdict(input_),
                    request.POST,
                    request.FILES,
                    instance=user.profile)

                if f.is_valid():
                    f.save()
                    return MutationNormalOutput(success=True)
                else:
                    return MutationNormalOutput(
                        success=False, errors=f.errors.get_json_data()
                    )

            except Exception:
                error_message = f'Failed to update avatar of user:\
                        {user}'
                error_code = 'avatar_update_error'
                return MutationNormalOutput(
                    success=False,
                    errors=[
                        {
                            "message": error_message,
                            "code": error_code
                        }
                    ]
                )

        return MutationNormalOutput(
            success=True,
            errors=[])


@strawberry.type
class UserMutation:
    """
    User Mutations
    """

    # Custom graphql_auth mutations
    register = Register.field
    send_password_reset_email = SendPasswordResetEmail.field

    # graphql_auth mutations
    verify_account = VerifyAccount.field
    resend_activation_email = mutations.ResendActivationEmail.field
    password_reset = mutations.PasswordReset.field
    password_change = mutations.PasswordChange.field
    archive_account = mutations.ArchiveAccount.field
    delete_account = DeleteAccount.field
    update_account = mutations.UpdateAccount.field

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.field
    verify_token = mutations.VerifyToken.field
    refresh_token = mutations.RefreshToken.field
    revoke_token = mutations.RevokeToken.field
    update_avatar = UpdateAvatar.field
