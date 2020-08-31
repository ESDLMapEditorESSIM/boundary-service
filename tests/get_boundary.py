#  This work is based on original code developed and copyrighted by TNO 2020.
#  Subsequent contributions are licensed to you by the developers of such code and are
#  made available to the Project under one or several contributor license agreements.
#
#  This work is licensed to you under the Apache License, Version 2.0.
#  You may obtain a copy of the license at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#      TNO         - Initial implementation
#  Manager:
#      TNO

from config import config_dict
from os import environ

import psycopg2
from postgis import MultiPolygon
from postgis.psycopg import register

get_config_mode = environ.get('BOUNDARY_SERVICE_CONFIG_MODE', 'Debug')

try:
    config_mode = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid BOUNDARY_SERVICE_CONFIG_MODE environment variable entry.')

if __name__ == '__main__':
    pguri = config_mode.POSTGIS_DATABASE_URI
    print(pguri)

    db = psycopg2.connect(pguri)
    register(db)
    cursor = db.cursor()

    cursor.execute('SELECT geom FROM gem_2018 WHERE gm_code = \'GM0060\'')
    geom = cursor.fetchone()[0]
    print(geom)
