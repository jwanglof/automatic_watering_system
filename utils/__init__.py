blinker_signals = {
    'open_valve': 'OPEN_VALVE',
    'close_valve': 'CLOSE_VALVE',
    'add_valve': 'ADD_VALVE',
    'pump_is_on': 'PUMP_IS_ON',
    'pump_is_off': 'PUMP_IS_OFF'
}

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

DB_TABLES = {
    DB_AWS: [
        TABLE_STATISTICS,
        TABLE_PLANT,
        TABLE_OWN_PLANT
    ]
}
