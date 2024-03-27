#!/usr/bin/env python3
import os
import sys

if __name__ == "__main__":
    assert "BUILD_ENV" in os.environ, "BUILD_ENV not set in environment"
    build_env = os.environ["BUILD_ENV"]
    os.environ["DJANGO_SETTINGS_MODULE"] = "paskoocheh.settings." + build_env

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
