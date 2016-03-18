#!/usr/bin/env python
# coding=utf-8
import uuid
from inspect import currentframe
from threading import Timer

from wiringx86 import GPIOGalileoGen2 as GPIO

from AWS.MagneticValve import MagneticValve
from AWS.Moisture import Moisture
from AWS.Temperature import Temperature
from utils.print_debug import print_debug

from utils.Database import Database


class AutomaticWateringSystem(object):
    """
    Main class for the Automatic Watering System (AWS)
    Will initiate the classes needed for a plant
    """

    instances = {}

    def __init__(self, uuid, name, temperature_pin=None, magnetic_valve_pin=None, moisture_pin=None,
                 debug=False, gpio_debug=False):
        """
        Constructor

        :type uuid: str
        :param uuid: The ID from the database

        :type name: str
        :param name: The name of the plant

        :type temperature_pin: int
        :param temperature_pin: Which pin the temperature sensor is attached to

        :type magnetic_valve_pin: int
        :param magnetic_valve_pin: Which pin the magnetic valve is attached to

        :type moisture_pin: int
        :param moisture_pin: Which pin the moisture sensor is attached to

        :type debug: bool
        :param debug:

        :type gpio_debug: bool
        :param gpio_debug: Specify if the debug should be on/off for the GPIO library
        """
        print_debug(debug, currentframe().f_code.co_name, u'Init %s' % name, __name__)
        all_params_str = u'UUID: {uuid}. Name: {name}. TP: {tp}. MVP: {mvp}. MP: {mp}'.format(
            uuid=uuid,
            name=name,
            tp=temperature_pin,
            mvp=magnetic_valve_pin,
            mp=moisture_pin
        )
        print_debug(debug, currentframe().f_code.co_name, all_params_str, __name__)

        # Add the new instance to the instances-list
        AutomaticWateringSystem.instances[uuid] = self

        self.__name = name
        self.__temperature_pin = temperature_pin
        self.__magnetic_valve_pin = magnetic_valve_pin
        self.__moisture_pin = moisture_pin
        self.debug = debug

        # Get a uuid for the class so we can identify easier
        # self.__uuid = str(uuid4())  # type: uuid4
        self.__uuid = uuid

        self.DB = Database()
        self.db_own_plant = self.DB.get_own_plant_from_id(self.get_uuid)
        self.db_plant = self.DB.get_plant_from_id(self.db_own_plant.get('plant_id'))
        self.db_pump = self.DB.get_pump_from_id(self.db_own_plant.get('pump_id'))

        # Get a new instance of the GPIO
        self.gpio = GPIO(debug=gpio_debug)  # type: GPIO

        # It has to be a magnetic valve connected!
        self.MagneticValve = None
        if magnetic_valve_pin is not None:
            print_debug(debug, currentframe().f_code.co_name,
                        'Initializing magnetic valve at pin %i' % magnetic_valve_pin, __name__)
            self.MagneticValve = MagneticValve(self.gpio, self.__uuid, magnetic_valve_pin,
                                               name, self.db_own_plant.get('pump_id'), debug)  # type: MagneticValve
        else:
            error = EnvironmentError
            error.message = 'A magnetic valve is needed!'
            raise error

        self.TemperatureSensor = None
        if temperature_pin is not None:
            print_debug(debug, currentframe().f_code.co_name,
                        'Initializing temperature sensor at pin %i' % temperature_pin, __name__)
            self.TemperatureSensor = Temperature(self.gpio, self.__uuid, temperature_pin,
                                                 name, 30, debug)  # type: Temperature

        self.MoistureSensor = None
        if moisture_pin is not None:
            print_debug(debug, currentframe().f_code.co_name,
                        'Initializing moisture sensor at pin %i' % moisture_pin, __name__)
            self.MoistureSensor = Moisture(self.gpio, self.__uuid, moisture_pin, name,
                                           self.db_plant.get('min_moisture'), self.db_plant.get('max_moisture'),
                                           debug)  # type: Moisture

        self.__run_count = 0
        self.active = True

        # Run a check directly when a new instance is created
        self.__start_new_timer(0)

    def __start_new_timer(self, time=60):
        """
        Starts a new timer

        :type time: int
        :param time: How many seconds the timer should be set to
        """
        new_timer_uuid = str(uuid.uuid4())

        print_debug(self.debug, currentframe().f_code.co_name,
                    u'New timer starting with time {time}. AWS name: {name}. Timer UUID: {uuid}'
                    .format(time=time, name=self.get_name, uuid=new_timer_uuid), __name__)

        self.timer = Timer(time, self.__run, [new_timer_uuid])
        self.timer.start()

    def __run(self, timer_id):
        """
        Run the different checks, and open the valve if needed!
        This function should not be called directly! Call __start_new_timer() instead!
        """
        self.__run_count += 1
        print_debug(self.debug, currentframe().f_code.co_name,
                    u'Timer executed. AWS name: {name}. Timer UUID: {timer_id}'
                    .format(name=self.get_name, timer_id=timer_id), __name__)
        print_debug(self.debug, currentframe().f_code.co_name, u'Run count: %s' % self.__run_count, __name__)
        temp_exceed = False
        moist_exceed = False

        if self.TemperatureSensor:
            temp_exceed = self.TemperatureSensor.has_exceeded_threshold()

        if self.MoistureSensor:
            moist_exceed = self.MoistureSensor.has_deceeded_threshold()

        print_debug(self.debug, currentframe().f_code.co_name, u'Temp exceed: %s' % str(temp_exceed), __name__)
        print_debug(self.debug, currentframe().f_code.co_name, u'Moist exceed: %s' % str(moist_exceed), __name__)

        if moist_exceed:
            # Try to open the valve
            self.MagneticValve.send_open_valve_signal()

        print_debug(self.debug, currentframe().f_code.co_name,
                    u'Timer done. AWS name: {name}. Timer UUID: {timer_id}'
                    .format(name=self.get_name, timer_id=timer_id), __name__)

        self.__start_new_timer(10)

    def cleanup(self):
        """
        Cleanup all the things!
        """
        print_debug(self.debug, currentframe().f_code.co_name,
                    u'Cleanup  ({name}, {uuid})!'.format(name=self.get_name, uuid=self.get_uuid), __name__)

        if self.TemperatureSensor:
            self.TemperatureSensor.cleanup()

        if self.MoistureSensor:
            self.MoistureSensor.cleanup()

        self.MagneticValve.cleanup()

        self.timer.cancel()

        self.gpio.cleanup()

    @property
    def get_name(self):
        return self.__name

    @property
    def get_uuid(self):
        return self.__uuid
