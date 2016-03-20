#!/usr/bin/env python
# coding=utf-8
from inspect import currentframe
from math import log

import utils.convert_voltage
from utils.pins import analogPins
from utils.print_debug import print_debug


# TODO: Setter for celsius threshold if the user wants to change it

class Temperature:
    """
    Temperature-class that helps to get some human-readable data from a temperature sensor
    One instance represents one sensor
    Info about the sensor: http://www.seeedstudio.com/wiki/Grove_-_Temperature_Sensor
    """

    def __init__(self, gpio, uuid, pin, name, celsius_threshold, debug=False):
        """
        Constructor

        :type gpio: GPIOGalileoGen2
        :param gpio: An instance of GPIOGalileoGen2

        :type uuid: uuid4
        :type uuid: Unique identifier the parent class created

        :type pin: int
        :param pin: Specify which pin the temperature sensor is attached to. Must be an analog pin!

        :type name: str
        :param name:

        :type celsius_threshold: int
        :param celsius_threshold: Specify the threshold of the sensor

        :type debug: bool
        :param debug:
        """
        print_debug(debug, currentframe().f_code.co_name, 'Init temperature for: %s' % name)
        all_params_str = u'UUID: {uuid}. Pin: {pin}. Name: {name}. Celsius threshold: {c_threshold}'.format(
            uuid=uuid,
            pin=pin,
            name=name,
            c_threshold=celsius_threshold
        )
        print_debug(debug, currentframe().f_code.co_name, all_params_str)

        # TODO The threshold should be fetched from the database!

        self.gpio = gpio
        self.uuid = uuid
        self.pin = pin
        self.analog_pin = analogPins.get(pin)
        self.__name = name
        self.__celsius_threshold = celsius_threshold
        self.debug = debug

        # TODO Implement this!!
        self.min_celsius = 0
        self.max_celsius = 0

        # Set the pin to analog input so we can get the temperature from it
        self.gpio.pinMode(self.analog_pin, self.gpio.ANALOG_INPUT)

        # The B-value is fetched from the different examples using the temperature sensor
        # The used thermistor's data sheet is here: http://www.electan.com/datasheets/TTC03.pdf
        self.b_value = 3975

    @property
    def get_name(self):
        return self.__name

    def has_exceeded_threshold(self):
        return self.get_celsius() > self.__celsius_threshold

    def has_deceeded_threshold(self):
        return self.get_celsius() < self.__celsius_threshold

    def get_celsius(self):
        # //convert to temperature via datasheet ;
        # 1 / (Math.log(resistance / 10000) / B + 1 / 298.15) - 273.15;
        celsius = 1 / (log(self.__get_resistance() / 10000) / self.b_value + 1 / 298.15) - 273.15
        print_debug(self.debug, currentframe().f_code.co_name, 'Current celsius: ' + str(celsius))
        return celsius

    def get_fahrenheit(self):
        # (celsius_temperature * (9 / 5)) + 32;
        fahrenheit = self.get_celsius() * 9 / 5 + 32
        print_debug(self.debug, currentframe().f_code.co_name, 'Current fahrenheit: ' + str(fahrenheit))
        return fahrenheit

    def get_raw_read(self):
        try:
            raw = self.gpio.analogRead(self.analog_pin)
        except KeyError:
            raw = 100
            print 'Could not read pin: {analog_pin}. Is the temperature sensor really connected to that analog pin?'\
                .format(analog_pin=self.pin)
        print_debug(self.debug, currentframe().f_code.co_name, 'Raw read: ' + str(raw))
        return raw

    @staticmethod
    def cleanup():
        """
        Don't really need any clean-up since the pin is analog
        """
        pass

    def __get_resistance(self):
        # TODO If we get None then the pins aren't set up correctly, should throw an error..?
        # if self.get_raw_read() is not None:

        # //get the resistance of the sensor;
        # var resistance = (1023 - a) * 10000 / a;
        resistance = (utils.convert_voltage.voltage_resolution - self.get_raw_read()) * 10000 / self.get_raw_read()
        print_debug(self.debug, currentframe().f_code.co_name, 'Resistance: ' + str(resistance))
        return resistance
