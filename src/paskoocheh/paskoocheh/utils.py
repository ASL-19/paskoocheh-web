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

import inspect

import strawberry
from strawberry.relay.types import NodeIterableType
from strawberry.relay.utils import from_base64, to_base64
from strawberry.types.info import Info
from strawberry.utils.await_maybe import AwaitableOrValue

from strawberry_django import relay
from strawberry_django.permissions import DjangoPermissionExtension, _desc
from strawberry_django.resolvers import django_resolver
from strawberry_django.utils.typing import UserType

from gqlauth.core.types_ import MutationNormalOutput

from typing import Optional, ClassVar, Callable, Any, cast
from typing_extensions import Self


@strawberry.type
class Connection(relay.ListConnectionWithTotalCount[strawberry.relay.NodeType]):
    """
    A strawberry connection to count the number of query results
    """

    @strawberry.field
    def edge_count(root, info: Info) -> Optional[int]:
        return len(root.edges)

    # Adding offset argument to custom connection
    @classmethod
    def resolve_connection(
        cls,
        nodes: NodeIterableType[strawberry.relay.NodeType],
        *,
        info: Info,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs: Any,
    ) -> AwaitableOrValue[Self]:

        # This implemntation is based on the graphene
        # implementation of first/offset pagination
        if offset:
            if after:
                offset += from_base64(after) + 1
            # input offset starts at 1 while the offset starts at 0
            after = to_base64("arrayconnection", offset - 1)

        conn = super().resolve_connection(
            nodes,
            info=info,
            before=before,
            after=after,
            first=first,
            last=last,
            **kwargs,
        )

        if inspect.isawaitable(conn):

            async def wrapper():
                resolved = await conn
                resolved.nodes = nodes
                return resolved

            return wrapper()

        conn = cast(Self, conn)
        conn.nodes = nodes
        return conn


class IsAuthenticatedMutation(DjangoPermissionExtension):
    """
        Mark a field as only resolvable by authenticated users. (For Mutations)
    """

    DEFAULT_ERROR_MESSAGE: ClassVar[str] = "User is not authenticated."
    SCHEMA_DIRECTIVE_DESCRIPTION: ClassVar[Optional[str]] = _desc(
        "Can only be resolved by authenticated users.",
    )

    @django_resolver(qs_hook=None)
    def resolve_for_user(
        self,
        resolver: Callable,
        user: Optional[UserType],
        *,
        info: Info,
        source: Any,
    ):
        if user is None or not user.is_authenticated or not user.is_active:
            return MutationNormalOutput(
                success=False,
                errors=[
                    {
                        "message": "Unauthenticated",
                        "code": "unauthenticated"
                    }
                ]
            )

        return resolver()


class IsAuthenticatedField(DjangoPermissionExtension):
    """
        Mark a field as only resolvable by authenticated users.
        (For Queries: fields)
    """

    DEFAULT_ERROR_MESSAGE: ClassVar[str] = "User is not authenticated."
    SCHEMA_DIRECTIVE_DESCRIPTION: ClassVar[Optional[str]] = _desc(
        "Can only be resolved by authenticated users.",
    )

    @django_resolver(qs_hook=None)
    def resolve_for_user(
        self,
        resolver: Callable,
        user: Optional[UserType],
        *,
        info: Info,
        source: Any,
    ):
        if user is None or not user.is_authenticated or not user.is_active:
            return None

        return resolver()


class IsAuthenticatedConnection(DjangoPermissionExtension):
    """
        Mark a field as only resolvable by authenticated users.
        (For Queries: connections)
    """

    DEFAULT_ERROR_MESSAGE: ClassVar[str] = "User is not authenticated."
    SCHEMA_DIRECTIVE_DESCRIPTION: ClassVar[Optional[str]] = _desc(
        "Can only be resolved by authenticated users.",
    )

    @django_resolver(qs_hook=None)
    def resolve_for_user(
        self,
        resolver: Callable,
        user: Optional[UserType],
        *,
        info: Info,
        source: Any,
    ):
        if user is None or not user.is_authenticated or not user.is_active:
            return []

        return resolver()
