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

from app.boundary import blueprint
from app.boundary.boundary import Boundary

boundary = Boundary()
boundary.db_connect()


@blueprint.route('/<scope_type>/<scope_id>')
def get_boundary(scope_type, scope_id):
    return boundary.get_boundary_REST(2019, "", scope_type, scope_id)


@blueprint.route('/<subscope_type>/<scope_type>/<scope_id>')
def get_sub_boundary(subscope_type, scope_type, scope_id):
    return boundary.get_sub_boundaries_REST(2019, "", subscope_type, scope_type, scope_id)


@blueprint.route('/YEAR/<year>/<scope_type>/<scope_id>')
def get_boundary_year(scope_type, scope_id, year):
    return boundary.get_boundary_REST(year, "", scope_type, scope_id)


@blueprint.route('/YEAR/<year>/<subscope_type>/<scope_type>/<scope_id>')
def get_sub_boundary_year(year, subscope_type, scope_type, scope_id):
    return boundary.get_sub_boundaries_REST(year, "", subscope_type, scope_type, scope_id)


@blueprint.route('/WGS/<scope_type>/<scope_id>')
def get_boundary_wgs(scope_type, scope_id):
    return boundary.get_boundary_REST(2019, "WGS", scope_type, scope_id)


@blueprint.route('/WGS/<scope_type>/<scope_id>/<year>')
def get_boundary_wgs_year(scope_type, scope_id, year):
    return boundary.get_boundary_REST(year, "WGS", scope_type, scope_id)
