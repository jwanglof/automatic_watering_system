#!/usr/bin/env python
# coding=utf-8
from inspect import currentframe
from uuid import uuid4

from wiringx86 import GPIOGalileoGen2 as GPIO

from utils.MagneticValve import MagneticValve
from utils.print_debug import print_debug
from utils.Temperature import Temperature
from utils.Moisture import Moisture


class AutomaticWateringSystem(object):
    """
    Main class for the Automatic Watering System (AWS)
    Will initiate the classes needed for a plant
    """
    def __init__(self, name, temperature_pin=None, magnetic_valve_pin=None, moisture_pin=None, debug=False):
        """
        Constructor

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
        """
        print_debug(debug, currentframe().f_code.co_name, 'Init %s' % name)

        self.__name = name
        self.__temperature_pin = temperature_pin
        self.__magnetic_valve_pin = magnetic_valve_pin
        self.__moisture_pin = moisture_pin
        self.debug = debug

        # Get a uuid for the class so we can identify easier
        self.__uuid = str(uuid4())  # type: uuid4

        # Get a new instance of the GPIO
        self.gpio = GPIO(debug=debug)  # type: GPIO

        if temperature_pin:
            self.TemperatureSensor = Temperature(self.gpio, self.__uuid, temperature_pin,
                                                 name, 30, debug)  # type: Temperature

        if magnetic_valve_pin:
            self.MagneticValve = MagneticValve(self.gpio, self.__uuid, magnetic_valve_pin,
                                               name, debug)  # type: MagneticValve

        if moisture_pin:
            self.MoistureSensor = Moisture(self.gpio, self.__uuid, moisture_pin, name, debug)  # type: Moisture

    def run(self):


    def cleanup(self):
        self.gpio.cleanup()

    @property
    def get_name(self):
        return self.__name

    @property
    def get_uuid(self):
        return self.__uuid
