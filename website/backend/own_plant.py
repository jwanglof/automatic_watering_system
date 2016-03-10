#!/usr/bin/env python
# coding=utf-8
import json

from flask import Blueprint, abort, g, request
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

import utils.Database as DB


blueprint = Blueprint('own_plant', __name__, url_prefix='/own_plant')


# The pattern we're using for managing database connections is to have **a connection per request**.
# We're using Flask's `@app.before_request` and `@app.teardown_request` for
# [opening a database connection](http://www.rethinkdb.com/api/python/connect/) and
# [closing it](http://www.rethinkdb.com/api/python/close/) respectively.
@blueprint.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=DB.RDB_HOST, port=DB.RDB_PORT, db=DB.DB_AWS)
    except RqlDriverError:
        abort(503, "No database connection could be established.")


@blueprint.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass


@blueprint.route('/')
def get_plants():
    selection = list(r.table(DB.TABLE_OWN_PLANT).run(g.rdb_conn))
    return json.dumps(selection)


@blueprint.route('/')
def new_plant():
    print request.json
