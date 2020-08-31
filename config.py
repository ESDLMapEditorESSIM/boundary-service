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

from os import environ


class Config(object):
    # PostgreSQL database
    POSTGIS_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        environ.get('BOUNDARY_SERVICE_DATABASE_USER', 'boundary_service'),
        environ.get('BOUNDARY_SERVICE_DATABASE_PASSWORD', 'password'),
        environ.get('BOUNDARY_SERVICE_DATABASE_HOST', 'postgres'),
        environ.get('BOUNDARY_SERVICE_DATABASE_PORT', 5432),
        environ.get('BOUNDARY_SERVICE_DATABASE_NAME', 'boundaries')
    )

    DEFAULT_CRS = "WGS"


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


class DebugConfig(Config):
    DEBUG = True


config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
