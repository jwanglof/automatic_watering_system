#!/usr/bin/env python
# coding=utf-8
import json

import rethinkdb as r
from flask import Blueprint, abort, g, render_template, redirect, url_for
from rethinkdb.errors import RqlDriverError

import utils.Database as DB
from website.forms.PlantForm import PlantForm


blueprint = Blueprint('plant', __name__, url_prefix='/plant')


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
    """Return all plants in a list"""
    plants = list(r.table(DB.TABLE_PLANT).run(g.rdb_conn))
    return render_template('plant/all_plants.html', plants=json.dumps(plants))


@blueprint.route('/<string:get_id>', methods=['GET'])
def get_plant(get_id):
    """Get a specific plant
    :type get_id: str
    :param get_id:
    """
    selection = r.table(DB.TABLE_PLANT).get(get_id).run(g.rdb_conn)
    return json.dumps(selection)


@blueprint.route('/add', methods=['GET', 'POST'])
def new_plant():
    """Create a new own plant"""
    form = PlantForm()
    if form.is_submitted():
        if form.validate():
            inserted = r.table(DB.TABLE_PLANT).insert(form.data).run(g.rdb_conn)
            # return jsonify(id=inserted['generated_keys'][0])
            return redirect(url_for('plant.get_plants'))
        else:
            abort(400, form.errors)

    return render_template('plant/add_plant.html', form=form)


@blueprint.route('/<string:delete_id>', methods=['DELETE'])
def delete_plant(delete_id):
    """Delete a plant
    :type delete_id: str
    :param delete_id:
    """
    deletion = r.table(DB.TABLE_PLANT).get(delete_id).delete().run(g.rdb_conn)
    if deletion.get('deleted') is 1:
        return delete_id
    else:
        abort(400, 'Invalid ID!')
