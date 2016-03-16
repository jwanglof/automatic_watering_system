#!/usr/bin/env python
# coding=utf-8
from datetime import datetime

import pytz as pytz

import rethinkdb as r

import utils.Database as DB


def utc_filter(value, time_format="%d/%m/%y %H:%M"):
    # timezone you want to convert to from UTC
    # More here: http://stackoverflow.com/questions/13866926/python-pytz-list-of-timezones

    if not isinstance(value, datetime):
        value = datetime.fromtimestamp(value)
    tz = pytz.timezone('Europe/Stockholm')
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(time_format)


def get_plant_from_id(plant_id):
    rdb_conn = r.connect(host=DB.RDB_HOST, port=DB.RDB_PORT, db=DB.DB_AWS)
    plant = r.table(DB.TABLE_PLANT).get(plant_id).run(rdb_conn)
    rdb_conn.close()
    return plant


def get_pump_from_id(pump_id):
    rdb_conn = r.connect(host=DB.RDB_HOST, port=DB.RDB_PORT, db=DB.DB_AWS)
    pump = r.table(DB.TABLE_PUMP).get(pump_id).run(rdb_conn)
    rdb_conn.close()
    return pump