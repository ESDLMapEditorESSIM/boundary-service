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

from app import create_app
from config import config_dict
from os import environ

get_config_mode = environ.get('BOUNDARY_SERVICE_CONFIG_MODE', 'Debug')

try:
    config_mode = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid BOUNDARY_SERVICE_CONFIG_MODE environment variable entry.')

app = create_app(config_mode)
app.run(host = '0.0.0.0', port = 4002)