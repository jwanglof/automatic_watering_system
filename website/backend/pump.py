#!/usr/bin/env python
# coding=utf-8
import json

import rethinkdb as r
from flask import Blueprint, abort, g, render_template, redirect, url_for
from rethinkdb.errors import RqlDriverError

import utils.Database as DB
from website.AWSError import AWSError
from website.forms.PumpForm import PumpForm

blueprint = Blueprint('pump', __name__, url_prefix='/pump')


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
def get_pumps():
    """Return all pumps in a list"""
    plants = list(r.table(DB.TABLE_PUMP).run(g.rdb_conn))
    return render_template('own_plant/all_own_plants.html', plants=json.dumps(plants))


@blueprint.route('/<string:get_id>', methods=['GET'])
def get_pump(get_id):
    """Get a specific pump
    :type get_id: str
    :param get_id:
    """
    selection = r.table(DB.TABLE_PUMP).get(get_id).run(g.rdb_conn)
    return json.dumps(selection)


@blueprint.route('/add', methods=['GET', 'POST'])
def new_pump():
    """Create a new pump"""
    # existing_plants = r.table(DB.TABLE_PLANT)
    #
    # form = OwnPlantForm()
    # # Populate the plant-drop down
    # form.plant_id.choices = [(p['id'], p['name'].capitalize()) for p in existing_plants.run(g.rdb_conn)]

    form = PumpForm()

    if form.is_submitted():
        if form.validate():
            inserted = r.table(DB.TABLE_PUMP).insert(form.data).run(g.rdb_conn)
            # return jsonify(id=inserted['generated_keys'][0])
            return redirect(url_for('pump.get_pumps'))
        else:
            # abort(400, form.errors)
            raise AWSError(form.errors, status_code=400)

    return render_template('pump/add_pump.html', form=form)


@blueprint.route('/<string:delete_id>', methods=['DELETE'])
def delete_plant(delete_id):
    """Delete a plant
    :type delete_id: str
    :param delete_id:
    """
    deletion = r.table(DB.TABLE_PUMP).get(delete_id).delete().run(g.rdb_conn)
    if deletion.get('deleted') is 1:
        return delete_id
    else:
        abort(400, 'Invalid ID!')
