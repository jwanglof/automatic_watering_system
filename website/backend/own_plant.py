#!/usr/bin/env python
# coding=utf-8
import json

from flask import Blueprint, abort, g, request, jsonify
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

import utils.Database as DB

from form_validation.OwnPlantValidation import OwnPlantValidation


blueprint = Blueprint('own_plant', __name__, url_prefix='/own_plant')


# Add the testing-variable to the blueprint so we can know if we're in testing mode or not
@blueprint.record
def record_params(setup_state):
    blueprint.testing = setup_state.app.config.get('TESTING')
    if blueprint.testing:
        blueprint.database_name = setup_state.app.config.get('DB_NAME')


# The pattern we're using for managing database connections is to have **a connection per request**.
# We're using Flask's `@app.before_request` and `@app.teardown_request` for
# [opening a database connection](http://www.rethinkdb.com/api/python/connect/) and
# [closing it](http://www.rethinkdb.com/api/python/close/) respectively.
@blueprint.before_request
def before_request():
    db_name = DB.DB_AWS
    if blueprint.testing:
        db_name = blueprint.database_name

    try:
        g.rdb_conn = r.connect(host=DB.RDB_HOST, port=DB.RDB_PORT, db=db_name)
    except RqlDriverError:
        abort(503, "No database connection could be established.")


@blueprint.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass


@blueprint.route('/', methods=['GET'])
def get_plants():
    selection = list(r.table(DB.TABLE_OWN_PLANT).run(g.rdb_conn))
    return json.dumps(selection)


@blueprint.route('/', methods=['POST'])
def new_plant():
    form = OwnPlantValidation.from_json(request.get_json())
    if form.validate():
        inserted = r.table(DB.TABLE_OWN_PLANT).insert(request.get_json()).run(g.rdb_conn)
        return jsonify(id=inserted['generated_keys'][0])
    else:
        abort(400, form.errors)
