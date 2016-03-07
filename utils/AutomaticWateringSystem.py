#!/usr/bin/env python
# coding=utf-8
from wiringx86 import GPIOGalileoGen2 as GPIO

from utils.print_debug import print_debug


class AutomaticWateringSystem(object):

    def __init__(self, debug):
        self.debug = debug

        # Get a new instance of the GPIO
        self.gpio = GPIO(debug=debug)

        # self.queue = WateringQueue()

        # self.__setup_temperature(temperature_pin)

    # def __setup_temperature(self, temperature_pin):
    #     self.GetTemperature = Temperature(self.gpio, analogPins.get(temperature_pin))

    # # def get_temperature(self, celsius=True, fahrenheit=False, raw=False):
    # def get_temperature(self, **kwargs):
    #     # if kwargs.get('celsius'):
    #     # if celsius:
    #     if kwargs.get('fahrenheit'):
    #     # elif fahrenheit:
    #         return self.GetTemperature.get_fahrenheit()
    #     elif kwargs.get('raw'):
    #     # elif raw:
    #         return self.GetTemperature.get_current_read()
    #     else:
    #         return self.GetTemperature.get_celsius()

    def print_debug(self, func_name, text):
        print_debug(self.debug, func_name, text)
        # if self.debug:
        #     now = datetime.now().strftime("%B %d %I:%M:%S")
        #     print '{0} {1: <20}{2}'.format(now, func_name + ':', text)
