#!/usr/bin/env python
# coding=utf-8
from time import time
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, ReqlUserError

DB_AWS = 'aws'

TABLE_STATISTICS = 'statistics'
TABLE_STATISTICS_CREATED = 'created'
TABLE_STATISTICS_TYPE = 'type'
TABLE_STATISTICS_PLANT_ID = 'plant_id'
TABLE_STATISTICS_RAW_MOISTURE = 'raw_moisture'
TABLE_STATISTICS_RAW_TEMPERATURE = 'raw_temperature'

TABLE_PLANT = 'plant'
TABLE_PLANT_CREATED = 'created'
TABLE_PLANT_NAME = 'name'
TABLE_PLANT_MAX_TEMPERATURE = 'max_temperature'
TABLE_PLANT_MIN_TEMPERATURE = 'min_temperature'
TABLE_PLANT_MAX_MOISTURE = 'max_moisture'
TABLE_PLANT_MIN_MOISTURE = 'min_moisture'


class Database:

    def __init__(self, db_host=None, db_port=None):
        self.db_host = db_host or '10.0.0.50'
        self.db_port = db_port or 28015


        # self.tables = {
        #     'temperature': {
        #         'raw_value': 'raw_value',
        #         'plant_id': 'plant_id',
        #         'moisture_id': 'moisture_id',
        #         'created': 'created'
        #     },
        #     'plant': {
        #         'created': 'created'
        #     },
        #     'moisture': {
        #         'raw_value': 'raw_value',
        #         'plant_id': 'plant_id',
        #         'temperature_id': 'temperature_id',
        #         'created': 'created'
        #     }
        # }

        self.tables = {
            DB_AWS: [
                TABLE_STATISTICS,
                TABLE_PLANT
            ]
        }

        self.connection = r.connect(host=self.db_host, port=self.db_port)
        try:
            for database, tables in self.tables.iteritems():
                r.db_create(database).run(self.connection)
                for t in tables:
                    r.db(database).table_create(t).run(self.connection)
        except RqlRuntimeError:
            print 'Database already exist'
        finally:
            self.connection.close()

    def __setup_connection(self):
        self.connection = r.connect(host=self.db_host, port=self.db_port, db=DB_AWS)
        return self.connection

    def __tear_down_connection(self):
        self.connection.close()

    # def add_statistic(self, moisture, temperature, plant_id):
    def add_statistic(self, **kwargs):
        self.__setup_connection()
        r.db(DB_AWS).table(TABLE_STATISTICS).insert({
            TABLE_STATISTICS_CREATED: time(),
            TABLE_STATISTICS_RAW_MOISTURE: kwargs.get('moisture', 0),
            TABLE_STATISTICS_RAW_TEMPERATURE: kwargs.get('temperature', 0)#,
            # TABLE_STATISTICS_PLANT_ID: kwargs.get('plant_id', )
        }).run(self.connection)
        self.__tear_down_connection()

    def add_plant(self, **kwargs):
        # Name is required
        if kwargs.get('name') is not None:
            self.__setup_connection()
            r.db(DB_AWS).table_create(TABLE_PLANT).insert({
                TABLE_PLANT_CREATED: time(),
                TABLE_PLANT_NAME: kwargs.get('name'),
                TABLE_PLANT_MAX_TEMPERATURE: kwargs.get('max_temperature', 125),
                TABLE_PLANT_MIN_TEMPERATURE: kwargs.get('min_temperature', -40),
                TABLE_PLANT_MAX_MOISTURE: kwargs.get('max_moisture', 1),
                TABLE_PLANT_MIN_MOISTURE: kwargs.get('min_moisture', 0)
            })
            self.__tear_down_connection()
        else:
            raise ReqlUserError
