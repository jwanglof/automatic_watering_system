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
from website.test_backend.test_base import BaseTest

DB_AWS_TEST = ''.join(choice(ascii_uppercase + digits) for _ in range(10))


class OwnPlantTestCase(BaseTest):
    def test_add_own_plants(self):
        """Will add one own plant"""
        path = self._create_own_plant_data('Nope', 'Lol')
        data = json.loads(path.data)
        self.assertEqual(path.status_code, 200)
        self.assertIsNotNone(data.get('id', None))
        self.assertEqual(len(list(r.table(DB.TABLE_PLANT).run(self.connection))), 1)
    
        # Add another one
        path2 = self._create_own_plant_data('Nope2', 'Luuulz')
        self.assertEqual(path2.status_code, 200)
        self.assertEqual(len(list(r.table(DB.TABLE_PLANT).run(self.connection))), 2)
    
    def test_fail_add_own_plant(self):
        """Will fail since we don't provide a plant_id"""
        data = dict(
            not_plant_id='trolll',
            description='Finizz'
        )
        path = self.app.post('/plant/add',
                             data=json.dumps(data),
                             content_type='application/json')
        self.assertEquals(path.status_code, 400)
    
    def test_get_one_plant(self):
        """Will get the newly created plant"""
        post_path = self._create_own_plant_data('Test', 'Hejz')
        post_path_json_data = json.loads(post_path.data)
        new_id = post_path_json_data.get('id', None)
    
        # Make sure that we got an ID
        self.assertIsNotNone(new_id)
    
        get_path = self.app.get('/own_plant/' + new_id)
        get_path_json_data = json.loads(get_path.data)
        self.assertEqual(get_path.status_code, 200)
        self.assertIsNot(get_path.data, 'null')
        self.assertIsInstance(get_path_json_data, dict)
        self.assertIsNotNone(get_path_json_data.get('id', None))
    
    def test_delete_one_plant(self):
        """Will delete the newly created plant"""
        post_path = self._create_own_plant_data('Test', 'Hejz')
        post_path_json_data = json.loads(post_path.data)
        new_id = post_path_json_data.get('id', None)
    
        # Make sure we got an ID
        self.assertIsNotNone(new_id)
    
        delete_path = self.app.delete('/own_plant/' + new_id)
        self.assertIsNotNone(delete_path.data)
        self.assertIsInstance(delete_path.data, str)
        self.assertEqual(delete_path.status_code, 200)
    
    def test_fail_delete_one_plant(self):
        """Will fail since we provides an ID that doesn't exist"""
        delete_path = self.app.delete('/own_plant/id-that-does-not-exist')
        self.assertEqual(delete_path.status_code, 400)
