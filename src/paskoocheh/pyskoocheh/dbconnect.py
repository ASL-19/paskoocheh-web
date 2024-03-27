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

import psycopg2
import pymysql


def psql_connect(config):
    """
        Connect to the RDS database
    """

    try:
        conn = psycopg2.connect(
            "host={} "
            "port={} "
            "user={} "
            "password={} "
            "dbname={} "
            "connect_timeout={} ".format(
                config['HOST'], config['PORT'], config['USER'], config['PASSWORD'], config['DB_NAME'], config['TIMEOUT'])
        )
        return conn

    except Exception:
        return None


def mysql_connect(config):
    """
        Connect to the RDS database
    """

    try:
        conn = pymysql.connect(
            host=config['HOST'],
            port=config['PORT'],
            user=config['USER'],
            passwd=config['PASSWORD'],
            db=config['DB_NAME'],
            connect_timeout=config['TIMEOUT']
        )
        return conn

    except Exception:
        return None
