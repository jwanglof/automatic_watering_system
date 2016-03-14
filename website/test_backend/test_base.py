#!/usr/bin/env python
# coding=utf-8
import json
import unittest
from random import choice
from string import ascii_uppercase, digits

import rethinkdb as r
from flask.ext.wtf.csrf import generate_csrf
from rethinkdb.errors import RqlRuntimeError

import utils.Database as DB
import website.app as app
# DB_AWS_TEST = 'aws_test'
from website.app_settings import TestingConfig

DB_AWS_TEST = ''.join(choice(ascii_uppercase + digits) for _ in range(10))


class BaseTest(unittest.TestCase):
    connection = None

    @classmethod
    def setUpClass(cls):
        cls.connection = r.connect(host=DB.RDB_HOST, port=DB.RDB_PORT, db=DB_AWS_TEST)
        try:
            # Create the DB tables we need
            DB.Database.create_db_structure(DB_AWS_TEST)
            test_conf = TestingConfig(DB_AWS_TEST)
            cls.app = app.create_app(test_conf).test_client()
            # print 'Set-up DONE. DB-name: {db_name}'.format(db_name=DB_AWS_TEST)
        except RqlRuntimeError:
            # print 'The test-database already exist. Will remove it, and then re-run the test!'
            r.db_drop(DB_AWS_TEST).run(cls.connection)
            cls.setUpClass()

    @classmethod
    def tearDownClass(cls):
        r.db_drop(DB_AWS_TEST).run(cls.connection)
        cls.connection.close()
        # print 'Tear-down DONE'

    def setUp(self):
        # Delete all data from all tables so we start clean before all tests
        DB.Database.delete_db_data(self.connection, DB_AWS_TEST)

    def _create_own_plant_data(self, plant_id, **kwargs):
        data = dict(
            plant_id=plant_id,
            description=kwargs.get('description', ''),
            temperature_pin=kwargs.get('temperature_pin', None),
            moisture_pin=kwargs.get('moisture_pin', None),
            magnetic_valve_pin=kwargs.get('magnetic_valve_pin', None)
        )
        return self.app.post('/own_plant/add',
                             data=json.dumps(data),
                             content_type='application/json')

    def __create_plant_data(self, name, **kwargs):
        data = dict(
            name=name
        )

        if DB.TABLE_PLANT_MAX_MOISTURE in kwargs:
            print 111111

        return self.app.post('/plant/',
                             data=json.dumps(data),
                             content_type='application/json')
