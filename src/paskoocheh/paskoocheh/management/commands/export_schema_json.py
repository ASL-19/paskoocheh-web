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
import pathlib
import sys

from django.core.management.base import BaseCommand, CommandError
from strawberry import Schema
from strawberry.printer import print_schema
from strawberry.utils.importer import import_module_symbol

from paskoocheh.schema import schema


class Command(BaseCommand):
    help = "Export the graphql schema"  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument("schema", nargs=1, type=str, help="The schema location")
        parser.add_argument("--path", nargs="?", type=str, help="Optional path to export")

    def handle(self, *args, **options):
        try:
            schema_symbol = import_module_symbol(options["schema"][0], default_symbol_name="schema")
        except (ImportError, AttributeError) as e:
            raise CommandError(str(e)) from e

        if not isinstance(schema_symbol, Schema):
            raise CommandError("The `schema` must be an instance of strawberry.Schema")

        schema_output = print_schema(schema_symbol)
        path = options.get("path")
        if path:
            if path and path.endswith('.json'):
                schema_output = json.dumps(
                    {
                        "data": schema.introspect()
                    },
                    indent=4,
                    sort_keys=True
                )
            with pathlib.Path(path).open("w") as f:
                f.write(schema_output)
        else:
            sys.stdout.write(schema_output)
