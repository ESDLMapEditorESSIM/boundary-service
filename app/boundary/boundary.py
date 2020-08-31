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

# from shapely import geometry, wkb


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


class Boundary:

    def __init__(self):
        self.db = None
        self.cursor = None
        self.config_mode = None
        self.boundary_cache = dict()
        self.scope_mapping = scope_mapping

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

    def get_boundary_REST(self, year, crs, scope_type, scope_id):
        year_int = int(year)

        boundary_cache_key = str(year)+crs+scope_type+scope_id
        if boundary_cache_key in self.boundary_cache:
            print("returning from cache...")
            return json.dumps(self.boundary_cache[boundary_cache_key])

        try:
            self.db.isolation_level
        except psycopg2.OperationalError as oe:
            self.db_connect()

        if crs == "":
            crs = self.config_mode.DEFAULT_CRS

        if year_int in allowed_years and crs in crs_mapping and scope_type in allowed_scopes_for_boundary:
            table_name = self.scope_mapping[scope_type]["table_name_prefix"] + '_' + str(year) + crs_mapping[crs]
            select = '{}_code, {}_naam, geom'.format(self.scope_mapping[scope_type]["field_name_prefix"],self.scope_mapping[scope_type]["field_name_prefix"])
            query = 'SELECT {} FROM {} WHERE {}_code = \'{}\''.format(select, table_name, self.scope_mapping[scope_type]["field_name_prefix"], scope_id)

            try:
                print("Running query: {}".format(query))
                self.cursor.execute(query)
            except:
                print("Exception during query, probably lost database connection. Reconnecting...")
                self.db_connect()
                self.cursor.execute(query)

            qres = self.cursor.fetchone()

            if qres:
                code = qres[0]
                name = qres[1]
                geom = qres[2]

                result = {
                    "code": code,
                    "name": name,
                    "geom": geom.geojson
                }

                self.boundary_cache[boundary_cache_key] = result
                return json.dumps(result)
            else:
                return "Query returned no result, probably non existing scope_id", 404
        else:
            if not year_int in allowed_years:
                return "Year not allowed", 404
            if not crs in crs_mapping:
                return "CRS not allowed (only 'WGS' and 'RD' are supported)", 404
            if not scope_type in self.scope_mapping:
                return "Unknown scope type", 404
            return "Unknown error", 404

    def get_sub_boundaries_REST(self, year, crs, subscope_type, scope_type, scope_id):
        year_int = int(year)

        boundary_cache_key = str(year)+crs+subscope_type+scope_type+scope_id
        if boundary_cache_key in self.boundary_cache:
            print("returning from cache...")
            return json.dumps(self.boundary_cache[boundary_cache_key])

        try:
            self.db.isolation_level
        except psycopg2.OperationalError as oe:
            self.db_connect()

        if crs == "":
            crs = self.config_mode.DEFAULT_CRS

        if year_int in allowed_years \
                and crs in crs_mapping \
                and scope_type in self.scope_mapping\
                and subscope_type in allowed_scopes_for_subboundary:

            if scope_type in ['municipalities','districts','neighbourhoods']:
                table_name = self.scope_mapping[subscope_type]["table_name_prefix"] + '_' + str(year) + crs_mapping[crs]
                select = '{}_code, {}_naam, geom'.format(self.scope_mapping[subscope_type]["field_name_prefix"],self.scope_mapping[subscope_type]["field_name_prefix"])
                query = 'SELECT {} FROM {} WHERE {}_code = \'{}\''.format(select, table_name, self.scope_mapping[scope_type]["field_name_prefix"], scope_id)
            else:
                table_name = self.scope_mapping[subscope_type]["table_name_prefix"] + '_' + str(year) + crs_mapping[crs]
                select = '{}_code, {}_naam, geom'.format(self.scope_mapping[subscope_type]["field_name_prefix"],self.scope_mapping[subscope_type]["field_name_prefix"])

                subquery = 'SELECT {}_code FROM public.{} WHERE {}_code = \'{}\''.format(
                    self.scope_mapping[subscope_type]["field_name_prefix"],
                    self.scope_mapping[scope_type]["table_name"],
                    self.scope_mapping[scope_type]["field_name_prefix"],
                    scope_id)
                query = 'SELECT {} FROM {} WHERE {}_code in ({})'.format(
                    select,
                    table_name,
                    self.scope_mapping[subscope_type]["field_name_prefix"],
                    subquery)

            try:
                print("Running query: {}".format(query))
                self.cursor.execute(query)
            except:
                print("Exception during query, probably lost database connection. Reconnecting...")
                self.db_connect()
                self.cursor.execute(query)

            qres = self.cursor.fetchall()

            if qres:

                result_list = []

                for qr in qres:
                    code = qr[0]
                    name = qr[1]
                    geom = qr[2]

                    result = {
                        "code": code,
                        "name": name,
                        "geom": geom.geojson
                    }
                    result_list.append(result)

                self.boundary_cache[boundary_cache_key] = result_list
                return json.dumps(result_list)
            else:
                return "Query returned no result, probably non existing scope_id", 404
        else:
            if not year in allowed_years:
                return "Year not allowed", 404
            if not crs in crs_mapping:
                return "CRS not allowed (only 'WGS' and 'RD' are supported)", 404
            if not scope_type in self.scope_mapping:
                return "Unknown scope type", 404
            return "Unknown error", 404