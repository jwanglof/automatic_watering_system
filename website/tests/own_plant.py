#!/usr/bin/env python
# coding=utf-8
import unittest
import website.create_app as app

DB_AWS_TEST = 'aws_test'

class OwnPlantTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd