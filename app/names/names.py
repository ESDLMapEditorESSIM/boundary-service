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
from config import config_dict

import json
import psycopg2
from postgis import MultiPolygon
from postgis.psycopg import register


scope_mapping = {
    "countries": {
        "table_name": "bu_wk_gm_es_pv_la_2019",
        "table_name_prefix": "land",
        "field_name_prefix": "la"
    },
    "regions": {
        "table_name": "bu_wk_gm_es_pv_la_2019",
        "table_name_prefix": "res",
        "field_name_prefix": "es"
    },
    "provinces": {
        "table_name": "bu_wk_gm_es_pv_la_2019",
        "table_name_prefix": "prov",
        "field_name_prefix": "pv"
    },
    "municipalities": {
        "table_name": "bu_wk_gm_es_pv_la_2019",
        "table_name_prefix": "gem",
        "field_name_prefix": "gm"
    },
    "districts": {
        "table_name": "bu_wk_gm_es_pv_la_2019",
        "table_name_prefix": "wijk",
        "field_name_prefix": "wk"
    },
    "neighbourhoods": {
        "table_name": "bu_wk_gm_es_pv_la_2019",
        "table_name_prefix": "buurt",
        "field_name_prefix": "bu"
    }
}

allowed_years = [2019]
allowed_scopes_for_boundary = ["countries", "provinces", "regions", "municipalities", "districts", "neighbourhoods"]
allowed_scopes_for_subboundary = ["provinces", "regions", "municipalities", "districts", "neighbourhoods"]
crs_mapping = {
    "WGS": "_wgs"
}


class Names:

    def __init__(self):
        self.db = None
        self.cursor = None
        self.config_mode = None
        self.names_cache = dict()
        self.scope_mapping = scope_mapping
        self.allowed_scopes_for_boundary = allowed_scopes_for_boundary
        self.allowed_scopes_for_subboundary = allowed_scopes_for_subboundary

    def db_connect(self):
        config_mode = None
        get_config_mode = environ.get('BOUNDARY_SERVICE_CONFIG_MODE', 'Debug')

        try:
            self.config_mode = config_dict[get_config_mode.capitalize()]
        except KeyError:
            exit('Error: Invalid BOUNDARY_SERVICE_CONFIG_MODE environment variable entry.')

        pguri = self.config_mode.POSTGIS_DATABASE_URI

        self.db = psycopg2.connect(pguri)
        register(self.db)
        self.cursor = self.db.cursor()
        if self.db:
            print("Connected to DB")

    def get_names(self, year, scope_type, select_scope_type = None, select_scope_id = None):
        year_int = int(year)
        crs = self.config_mode.DEFAULT_CRS

        names_cache_key = str(year_int)+scope_type
        if select_scope_type is not None:
            names_cache_key = names_cache_key + select_scope_type
        if select_scope_id is not None:
            names_cache_key = names_cache_key + select_scope_id
        if names_cache_key in self.names_cache:
            print("returning from cache...")
            return json.dumps(self.names_cache[names_cache_key])

        try:
            self.db.isolation_level
        except psycopg2.OperationalError as oe:
            self.db_connect()

        select_scope = ""
        where_clause = ""

        if select_scope_type:
            if not(scope_type in self.allowed_scopes_for_subboundary) or\
                    (self.allowed_scopes_for_boundary.index(scope_type) <= self.allowed_scopes_for_boundary.index(select_scope_type)):
                error = "You cannot select {} names for the selection {}".format(scope_type, select_scope_type)
                print(error)
                return error, 404
            else:
                select_scope = '{}_code, {}_naam, '.format(
                    self.scope_mapping[select_scope_type]["field_name_prefix"],
                    self.scope_mapping[select_scope_type]["field_name_prefix"])
                where_clause = ' WHERE {}_code = \'{}\''.format(
                    self.scope_mapping[select_scope_type]["field_name_prefix"],
                    select_scope_id)

        if year_int in allowed_years and scope_type in self.allowed_scopes_for_boundary:
            table_name = self.scope_mapping[scope_type]["table_name"]

            select = select_scope + '{}_code, {}_naam'.format(
                self.scope_mapping[scope_type]["field_name_prefix"],
                self.scope_mapping[scope_type]["field_name_prefix"])
            query = 'SELECT DISTINCT {} FROM {}'.format(select, table_name)
            order_clause = ' ORDER BY {}_naam'.format(self.scope_mapping[scope_type]["field_name_prefix"])
            query = query + where_clause + order_clause

            try:
                print("Running query: {}".format(query))
                self.cursor.execute(query)
            except:
                print("Exception during query, probably lost database connection. Reconnecting...")
                self.db_connect()
                self.cursor.execute(query)

            qres = self.cursor.fetchall()

            if qres:
                self.names_cache[names_cache_key] = qres
                return json.dumps(qres)
            else:
                return "Query returned no result", 404
        else:
            if not year_int in allowed_years:
                return "Year not allowed", 404
            if not scope_type in self.scope_mapping:
                return "Unknown scope type", 404
            return "Unknown error", 404
