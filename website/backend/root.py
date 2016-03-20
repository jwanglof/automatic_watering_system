#!/usr/bin/env python
# coding=utf-8
from flask import Blueprint, render_template, g, abort
import rethinkdb as r
from rethinkdb.errors import RqlDriverError

import utils.Database as DB

blueprint = Blueprint('root', __name__, url_prefix='/')


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


@blueprint.route('/')
def root():
    # form = OwnPlantForm.OwnPlantForm()
    stats = list(r.table(DB.TABLE_STATISTICS).order_by(r.desc(DB.TABLE_STATISTICS_CREATED)).limit(30).run(g.rdb_conn))
    return render_template('root.html', stats=stats)
