#!/usr/bin/env python
# coding=utf-8
import json
import unittest
from random import choice
from string import ascii_uppercase, digits

from flask import Flask

import website.app as app

import utils.Database as DB

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError


# DB_AWS_TEST = 'aws_test'
from website.app_settings import TestingConfig

DB_AWS_TEST = ''.join(choice(ascii_uppercase + digits) for _ in range(10))


class OwnPlantTestCase(unittest.TestCase):
    connection = None

    @classmethod
    def setUpClass(cls):
        cls.connection = r.connect(host=DB.RDB_HOST, port=DB.RDB_PORT, db=DB_AWS_TEST)
        try:
            # Create the DB tables we need
            DB.Database.create_db_structure(cls.connection, DB_AWS_TEST)
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

    def test_root_path(self):
        root_path = self.app.get('/')
        self.assertEqual(root_path.status_code, 200)

    def test_empty_db(self):
        path = self.app.get('/own_plant/')
        data = json.loads(path.data)
        self.assertEqual(path.status_code, 200)
        self.assertEqual(len(data), 0)

    def test_add_own_plants(self):
        data = dict(
            plant_id='Nope',
            description='Lol'
        )
        path = self.app.post('/own_plant/',
                             data=json.dumps(data),
                             content_type='application/json')
        data = json.loads(path.data)
        self.assertEqual(path.status_code, 200)
        self.assertIsNotNone(data.get('id', None))
        self.assertEqual(len(list(r.table(DB.TABLE_OWN_PLANT).run(self.connection))), 1)

        data2 = dict(
            plant_id='Nope2',
            description='Luuuulz'
        )
        self.app.post('/own_plant/',
                      data=json.dumps(data2),
                      content_type='application/json')
        self.assertEqual(len(list(r.table(DB.TABLE_OWN_PLANT).run(self.connection))), 2)

    def test_add_own_plant_fail(self):
        data = dict(
            not_plant_id='trolll',
            description='Finizz'
        )
        path = self.app.post('/own_plant/',
                             data=json.dumps(data),
                             content_type='application/json')
        self.assertEquals(path.status_code, 400)
