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

from app.names import blueprint
from flask import render_template
from app.names.names import Names

names = Names()
names.db_connect()


@blueprint.route('/<scope_type>')
def get_names(scope_type):
    return names.get_names(2019, scope_type)


@blueprint.route('/<select_scope_type>/<select_scope_id>/<scope_type>')
def get_names_selected(select_scope_type, select_scope_id, scope_type):
    return names.get_names(2019, scope_type, select_scope_type, select_scope_id)


@blueprint.route('/YEAR/<year>/<scope_type>')
def get_names_year(year, scope_type):
    return names.get_names(year, scope_type)


@blueprint.route('/YEAR/<year>/<select_scope_type>/<select_scope_id>/<scope_type>')
def get_names_selected_year(year, select_scope_type, select_scope_id, scope_type):
    return names.get_names(year, scope_type, select_scope_type, select_scope_id)