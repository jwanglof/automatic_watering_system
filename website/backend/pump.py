#!/usr/bin/env python
# coding=utf-8
import json

import rethinkdb as r
from flask import Blueprint, abort, g, render_template, redirect, url_for
from rethinkdb.errors import RqlDriverError

import utils.Database as DB
from utils.Pump import Pump
from website.AWSError import AWSError
from website.forms.PumpForm import PumpForm

from utils.class_instances import pumps, own_plants

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
    pumps = list(r.table(DB.TABLE_PUMP).run(g.rdb_conn))
    return render_template('pump/all_pumps.html', pumps=pumps)


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
    form = PumpForm()

    if form.is_submitted():
        if form.validate():
            inserted = r.table(DB.TABLE_PUMP).insert(form.data).run(g.rdb_conn)
            uuid = inserted['generated_keys'][0]

            # Create a new instance of a pump
            pumps[uuid] = Pump(uuid=uuid,
                               pin=form.data.get(form.pin.id),
                               name=form.data.get(form.name.id),
                               gpio_debug=False,
                               debug=True)

            # return jsonify(id=inserted['generated_keys'][0])
            return redirect(url_for('pump.get_pumps'))
        else:
            # abort(400, form.errors)
            raise AWSError(form.errors, status_code=400)

    return render_template('pump/add_pump.html', form=form)


@blueprint.route('/<string:delete_id>', methods=['DELETE'])
def delete_pump(delete_id):
    """Delete a pump and cleanup the own plants that are using it
    :type delete_id: str
    :param delete_id:
    """

    # Get all own plants that use the pump that is deleted so we can do some cleanup
    all_own_plants = r.table(DB.TABLE_OWN_PLANT).filter(
        lambda plant:
            (plant['pump_id'] == delete_id) &
            (plant['active']).default(False)
    ).get_field('id').run(g.rdb_conn)

    # Clean-up all the relevant own plants
    # Will set the own plant as not active, and turn off everything related to that plant
    for own_plant_id in all_own_plants:
        r.table(DB.TABLE_OWN_PLANT).get(own_plant_id).update({'active': False}).run(g.rdb_conn)
        aws = own_plants.get(own_plant_id)
        aws.cleanup()

    deletion = r.table(DB.TABLE_PUMP).get(delete_id).delete().run(g.rdb_conn)
    if deletion.get('deleted') is 1:
        return delete_id
    else:
        abort(400, 'Invalid ID!')
