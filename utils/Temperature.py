#!/usr/bin/env python
# coding=utf-8
from inspect import currentframe
from math import log

import convert_voltage
from utils.AutomaticWateringSystem import AutomaticWateringSystem


class Temperature(AutomaticWateringSystem):
    """
    Temperature-class that helps to get some human-readable data from a temperature sensor
    One instance represents one sensor
    Info about the sensor: http://www.seeedstudio.com/wiki/Grove_-_Temperature_Sensor
    """
    def __init__(self, pin, celsius_threshold, debug=False):
        """
        Constructor

        :type celsius_threshold: int
        :param celsius_threshold: Specify the threshold of the sensor

        :type pin: int
        :param pin: Specify which pin the temperature sensor is attached to. Must be an analog pin!

        :type debug: bool
        :param debug:
        """
        AutomaticWateringSystem.__init__(self, debug)

        # Set the pin to analog input so we can get the temperature from it
        self.gpio.pinMode(pin, self.gpio.ANALOG_INPUT)

        self.__celsius_threshold = celsius_threshold

        self.pin = pin

        # The B-value is fetched from the different examples using the temperature sensor
        # The used thermistor's data sheet is here: http://www.electan.com/datasheets/TTC03.pdf
        self.b_value = 3975

    def has_exceeded_threshold(self):
        return self.get_celsius() > self.__celsius_threshold

    def get_celsius(self):
        # //convert to temperature via datasheet ;
        # 1 / (Math.log(resistance / 10000) / B + 1 / 298.15) - 273.15;
        celsius = 1 / (log(self.__get_resistance() / 10000) / self.b_value + 1 / 298.15) - 273.15
        self.print_debug(currentframe().f_code.co_name, 'Current celsius: ' + str(celsius))
        return celsius

    def get_fahrenheit(self):
        # (celsius_temperature * (9 / 5)) + 32;
        fahrenheit = self.get_celsius() * 9 / 5 + 32
        self.print_debug(currentframe().f_code.co_name, 'Current fahrenheit: ' + str(fahrenheit))
        return fahrenheit

    def get_raw_read(self):
        raw = self.gpio.analogRead(self.pin)
        self.print_debug(currentframe().f_code.co_name, 'Raw read: ' + str(raw))
        return raw

    def __get_resistance(self):
        # //get the resistance of the sensor;
        # var resistance = (1023 - a) * 10000 / a;
        resistance = (convert_voltage.voltage_resolution - self.get_raw_read()) * 10000 / self.get_raw_read()
        self.print_debug(currentframe().f_code.co_name, 'Resistance: ' + str(resistance))
        return resistance
