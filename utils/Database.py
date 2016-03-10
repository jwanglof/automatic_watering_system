#!/usr/bin/env python
# coding=utf-8
from os import environ
from time import time
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, ReqlUserError

try:
    RDB_HOST = environ["RDB_HOST"]
    RDB_PORT = environ["RDB_PORT"]
except KeyError:
    RDB_HOST = 'localhost'
    RDB_PORT = '28015'

DB_AWS = 'aws'

TABLE_STATISTICS = 'statistics'
TABLE_STATISTICS_CREATED = 'created'
TABLE_STATISTICS_TYPE = 'type'
TABLE_STATISTICS_RAW_MOISTURE = 'raw_moisture'
TABLE_STATISTICS_RAW_TEMPERATURE = 'raw_temperature'
TABLE_STATISTICS_OWN_PLANT_ID = 'plant_id'  # 'foreign key' to own_plant.id

TABLE_PLANT = 'plant'
TABLE_PLANT_CREATED = 'created'
TABLE_PLANT_NAME = 'name'
TABLE_PLANT_MAX_TEMPERATURE = 'max_temperature'
TABLE_PLANT_MIN_TEMPERATURE = 'min_temperature'
TABLE_PLANT_MAX_MOISTURE = 'max_moisture'
TABLE_PLANT_MIN_MOISTURE = 'min_moisture'

TABLE_OWN_PLANT = 'own_plant'
TABLE_OWN_PLANT_CREATED = 'created'
TABLE_OWN_PLANT_PLANT_ID = 'plant_id'
TABLE_OWN_PLANT_DESCRIPTION = 'description'

# DB_TABLES = {
#     DB_AWS: [
#         TABLE_STATISTICS,
#         TABLE_PLANT,
#         TABLE_OWN_PLANT
#     ]
# }


class Database(object):

    def __init__(self, db_host=None, db_port=None):
        self.db_host = db_host or RDB_HOST
        self.db_port = db_port or RDB_PORT


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

        self.connection = r.connect(host=self.db_host, port=self.db_port)
        self.create_db_structure(self.connection)
        self.connection.close()

    def __setup_connection(self):
        self.connection = r.connect(host=self.db_host, port=self.db_port, db=DB_AWS)
        return self.connection

    def __tear_down_connection(self):
        self.connection.close()

    @staticmethod
    def create_db_structure(connection, database=DB_AWS):
        # Create the database if it doesn't exist
        if database not in r.db_list().run(connection):
            r.db_create(database).run(connection)

        # Add the tables if they doesn't exist
        existing_tables = r.db(database).table_list().run(connection)

        if TABLE_STATISTICS not in existing_tables:
            r.db(database).table_create(TABLE_STATISTICS).run(connection)

        if TABLE_PLANT not in existing_tables:
            r.db(database).table_create(TABLE_PLANT).run(connection)

        if TABLE_OWN_PLANT not in existing_tables:
            r.db(database).table_create(TABLE_OWN_PLANT).run(connection)

    @staticmethod
    def delete_db_data(connection, database=DB_AWS):
        """
        Delete all data from the different tables
        :param connection:
        :param database:
        :return:
        """
        r.db(database).table(TABLE_STATISTICS).delete().run(connection)
        r.db(database).table(TABLE_PLANT).delete().run(connection)
        r.db(database).table(TABLE_OWN_PLANT).delete().run(connection)

    # def add_statistic(self, moisture, temperature, plant_id):
    def add_statistic(self, **kwargs):
        self.__setup_connection()
        r.table(TABLE_STATISTICS).insert({
            TABLE_STATISTICS_CREATED: time(),
            TABLE_STATISTICS_RAW_MOISTURE: kwargs.get('moisture', 0),
            TABLE_STATISTICS_RAW_TEMPERATURE: kwargs.get('temperature', 0)#,
            # TABLE_STATISTICS_OWN_PLANT_ID: kwargs.get('own_plant_id', )
        }).run(self.connection)
        self.__tear_down_connection()

    def add_plant(self, **kwargs):
        # Name is required
        if kwargs.get('name') is not None:
            self.__setup_connection()
            r.table_create(TABLE_PLANT).insert({
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
