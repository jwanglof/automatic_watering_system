#!/usr/bin/env python
# coding=utf-8
import json

import rethinkdb as r
from flask import Blueprint, abort, g, render_template, redirect, url_for
from rethinkdb.errors import RqlDriverError

import utils.Database as DB
from AutomaticWateringSystem import AutomaticWateringSystem
from website.AWSError import AWSError
from website.forms.OwnPlantForm import OwnPlantForm

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
    """Return all own plants in a list"""
    plants = list(r.table(DB.TABLE_OWN_PLANT).run(g.rdb_conn))
    return render_template('own_plant/all_own_plants.html', plants=json.dumps(plants))


@blueprint.route('/<string:get_id>', methods=['GET'])
def get_plant(get_id):
    """Get a specific own plant
    :type get_id: str
    :param get_id:
    """
    selection = r.table(DB.TABLE_OWN_PLANT).get(get_id).run(g.rdb_conn)
    return json.dumps(selection)


@blueprint.route('/add', methods=['GET', 'POST'])
def new_plant():
    """Create a new own plant"""
    existing_plants = r.table(DB.TABLE_PLANT)

    # Don't allow the user to see the form if there isn't any plants added
    if existing_plants.count().run(g.rdb_conn) is 0:
        raise AWSError('You must add a plant before you can add anything else!', status_code=503)

    existing_pumps = r.table(DB.TABLE_PUMP)

    if existing_pumps.count().run(g.rdb_conn) is 0:
        raise AWSError('You must add a pump before you can add anything else!', status_code=503)

    form = OwnPlantForm()
    # Populate the plant-drop down
    form.plant_id.choices = [(p['id'], p['name'].capitalize()) for p in existing_plants.run(g.rdb_conn)]
    form.pump_id.choices = [(p['id'], p['name'].capitalize()) for p in existing_pumps.run(g.rdb_conn)]

    if form.is_submitted():
        if form.validate():
            inserted = r.table(DB.TABLE_OWN_PLANT).insert(form.data).run(g.rdb_conn)
            uuid = inserted['generated_keys'][0]

            # Add the newly added plant so we can execute reads on it!
            AutomaticWateringSystem(uuid=uuid,
                                    name=form.data['name'],
                                    temperature_pin=form.data.get(form.temperature_sensor_pin.id),
                                    magnetic_valve_pin=form.data.get(form.magnetic_valve_pin.id),
                                    moisture_pin=form.data.get(form.moisture_sensor_pin.id),
                                    debug=True,
                                    gpio_debug=False)

            # return jsonify(id=inserted['generated_keys'][0])
            return redirect(url_for('own_plant.get_plants'))
        else:
            abort(400, form.errors)

    return render_template('own_plant/add_own_plant.html', form=form, active_page='own_plant.new_plant')


@blueprint.route('/<string:delete_id>', methods=['DELETE'])
def delete_plant(delete_id):
    """Delete a plant
    :type delete_id: str
    :param delete_id:
    """
    deletion = r.table(DB.TABLE_OWN_PLANT).get(delete_id).delete().run(g.rdb_conn)
    if deletion.get('deleted') is 1:
        return delete_id
    else:
        abort(400, 'Invalid ID!')
