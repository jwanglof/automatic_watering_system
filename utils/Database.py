#!/usr/bin/env python
# coding=utf-8
from os import environ
from time import time

import rethinkdb as r
from rethinkdb.errors import ReqlUserError

try:
    RDB_HOST = environ["RDB_HOST"]
    RDB_PORT = environ["RDB_PORT"]
except KeyError:
    RDB_HOST = 'localhost'
    RDB_PORT = '28015'

DB_AWS = 'aws'

TABLE_STATISTICS = 'statistics'
TABLE_STATISTICS_CREATED = 'created'
TABLE_STATISTICS_MOISTURE_RAW = 'moisture_raw'
TABLE_STATISTICS_MOISTURE_PERCENT = 'moisture_percent'
TABLE_STATISTICS_MOISTURE_MIN_PERCENT = 'moisture_min_percent'
TABLE_STATISTICS_MOISTURE_MAX_PERCENT = 'moisture_max_percent'
TABLE_STATISTICS_TEMPERATURE_RAW = 'temperature_raw'
TABLE_STATISTICS_TEMPERATURE_CELSIUS = 'temperature_celsius'
TABLE_STATISTICS_TEMPERATURE_MIN_CELSIUS = 'temperature_min_celsius'
TABLE_STATISTICS_TEMPERATURE_MAX_CELSIUS = 'temperature_max_celsius'
TABLE_STATISTICS_OWN_PLANT_ID = 'plant_id'  # 'foreign key' to own_plant.id
TABLE_STATISTICS_RUN_COUNT = 'run_count'

TABLE_PLANT = 'plant'
TABLE_PLANT_CREATED = 'created'
TABLE_PLANT_NAME = 'name'
TABLE_PLANT_MAX_TEMPERATURE = 'max_temperature'
TABLE_PLANT_MIN_TEMPERATURE = 'min_temperature'
TABLE_PLANT_MAX_MOISTURE = 'max_moisture'
TABLE_PLANT_MIN_MOISTURE = 'min_moisture'

TABLE_OWN_PLANT = 'own_plant'
TABLE_OWN_PLANT_CREATED = 'created'
TABLE_OWN_PLANT_NAME = 'name'
TABLE_OWN_PLANT_PLANT_ID = 'plant_id'
TABLE_OWN_PLANT_PUMP_ID = 'pump_id'
TABLE_OWN_PLANT_DESCRIPTION = 'description'
TABLE_OWN_PLANT_TEMPERATURE_PIN = 'temperature_sensor_pin'
TABLE_OWN_PLANT_MOISTURE_PIN = 'moisture_sensor_pin'
TABLE_OWN_PLANT_MAGNETIC_VALVE_PIN = 'magnetic_valve_pin'

TABLE_PUMP = 'pump'
TABLE_PUMP_CREATED = 'created'
TABLE_PUMP_NAME = 'name'
TABLE_PUMP_LOCATION = 'location'
TABLE_PUMP_DESCRIPTION = 'description'
TABLE_PUMP_PIN = 'pin'
TABLE_PUMP_PIN_TYPE = 'pin_type'  # Analog, digital or PWM


class Database(object):
    connection = None

    def __init__(self, db_host=None, db_port=None):
        self.db_host = db_host or RDB_HOST
        self.db_port = db_port or RDB_PORT

    def __setup_connection(self):
        self.connection = r.connect(host=self.db_host, port=self.db_port, db=DB_AWS)
        return self.connection

    def __tear_down_connection(self):
        try:
            self.connection.close()
        except Exception:
            pass

    def create_db_structure(self, connection=connection, database=DB_AWS):
        if not connection:
            connection = self.__setup_connection()

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

        if TABLE_PUMP not in existing_tables:
            r.db(database).table_create(TABLE_PUMP).run(connection)

        self.__tear_down_connection()

    def delete_db_data(self, connection, database=DB_AWS):
        """
        Delete all data from the different tables
        :param connection:
        :param database:
        :return:
        """
        if not connection:
            connection = self.__setup_connection()

        r.db(database).table(TABLE_STATISTICS).delete().run(connection)
        r.db(database).table(TABLE_PLANT).delete().run(connection)
        r.db(database).table(TABLE_OWN_PLANT).delete().run(connection)
        r.db(database).table(TABLE_PUMP).delete().run(connection)

        self.__tear_down_connection()

    def get_all_active_own_plants(self):
        connection = self.__setup_connection()
        res = r.table(TABLE_OWN_PLANT).filter(r.row['active']).run(connection)
        self.__tear_down_connection()
        return res

    def get_all_pumps(self):
        connection = self.__setup_connection()
        res = r.table(TABLE_PUMP).run(connection)
        self.__tear_down_connection()
        return res

    def get_own_plant_from_id(self, uuid):
        if not uuid:
            raise IndexError

        self.__setup_connection()
        a = r.db(DB_AWS).table(TABLE_OWN_PLANT).get(uuid).run(self.connection)
        self.__tear_down_connection()
        return a

    def get_plant_from_id(self, uuid):
        if not uuid:
            raise IndexError

        self.__setup_connection()
        a = r.db(DB_AWS).table(TABLE_PLANT).get(uuid).run(self.connection)
        self.__tear_down_connection()
        return a

    def get_pump_from_id(self, uuid):
        if not uuid:
            raise IndexError

        self.__setup_connection()
        a = r.db(DB_AWS).table(TABLE_PUMP).get(uuid).run(self.connection)
        self.__tear_down_connection()
        return a

    # def add_statistic(self, moisture, temperature, plant_id):
    def add_statistic(self, own_plant_id, **kwargs):
        """
        Add statistics to the database

        :type own_plant_id: str
        :param own_plant_id:

        :param kwargs:
        """

        insert_dict = {
            TABLE_STATISTICS_CREATED: time(),
            TABLE_STATISTICS_OWN_PLANT_ID: own_plant_id
        }

        if kwargs.get(TABLE_STATISTICS_RUN_COUNT) is not None:
            insert_dict[TABLE_STATISTICS_RUN_COUNT] = kwargs.get(TABLE_STATISTICS_RUN_COUNT)

        if kwargs.get(TABLE_STATISTICS_MOISTURE_RAW) is not None:
            insert_dict[TABLE_STATISTICS_MOISTURE_RAW] = kwargs.get(TABLE_STATISTICS_MOISTURE_RAW)
            insert_dict[TABLE_STATISTICS_MOISTURE_MIN_PERCENT] = kwargs.get(TABLE_STATISTICS_MOISTURE_MIN_PERCENT)
            insert_dict[TABLE_STATISTICS_MOISTURE_MAX_PERCENT] = kwargs.get(TABLE_STATISTICS_MOISTURE_MAX_PERCENT)
            insert_dict[TABLE_STATISTICS_MOISTURE_PERCENT] = kwargs.get(TABLE_STATISTICS_MOISTURE_PERCENT)

        if kwargs.get(TABLE_STATISTICS_TEMPERATURE_RAW) is not None:
            insert_dict[TABLE_STATISTICS_TEMPERATURE_RAW] = kwargs.get(TABLE_STATISTICS_TEMPERATURE_RAW)
            insert_dict[TABLE_STATISTICS_TEMPERATURE_MIN_CELSIUS] = kwargs.get(TABLE_STATISTICS_TEMPERATURE_MIN_CELSIUS)
            insert_dict[TABLE_STATISTICS_TEMPERATURE_MAX_CELSIUS] = kwargs.get(TABLE_STATISTICS_TEMPERATURE_MAX_CELSIUS)
            insert_dict[TABLE_STATISTICS_TEMPERATURE_CELSIUS] = kwargs.get(TABLE_STATISTICS_TEMPERATURE_CELSIUS)

        if own_plant_id is not None:
            self.__setup_connection()
            r.table(TABLE_STATISTICS).insert(insert_dict).run(self.connection)
            self.__tear_down_connection()
        else:
            raise ReqlUserError

    # def add_plant(self, **kwargs):
    #     # Name is required
    #     if kwargs.get('name') is not None:
    #         self.__setup_connection()
    #         r.table_create(TABLE_PLANT).insert({
    #             TABLE_PLANT_CREATED: time(),
    #             TABLE_PLANT_NAME: kwargs.get('name'),
    #             TABLE_PLANT_MAX_TEMPERATURE: kwargs.get('max_temperature', None),
    #             TABLE_PLANT_MIN_TEMPERATURE: kwargs.get('min_temperature', None),
    #             TABLE_PLANT_MAX_MOISTURE: kwargs.get('max_moisture', None),
    #             TABLE_PLANT_MIN_MOISTURE: kwargs.get('min_moisture', None)
    #         })
    #         self.__tear_down_connection()
    #     else:
    #         raise ReqlUserError
