#!/usr/bin/env python
# coding=utf-8
from inspect import currentframe

from utils.pins import analogPins
from utils.print_debug import print_debug


class Moisture:
    """
    http://seeedstudio.com/wiki/Grove_-_Moisture_Sensor
    """

    DRY = 'dry'
    DRY_MIN = 0
    DRY_MAX = 300
    HUMID = 'humid'
    HUMID_MIN = 300
    HUMID_MAX = 700
    WATER = 'water'
    WATER_MIN = 700
    WATER_MAX = 950

    def __init__(self, gpio, uuid, pin, name, type, debug=False):
        """
        Constructor

        :type gpio: GPIOGalileoGen2
        :param gpio: An instance of GPIOGalileoGen2

        :type uuid: uuid4
        :type uuid: Unique identifier the parent class created

        :type pin: int
        :param pin: Specify which pin the moisture sensor is attached to. Must be an analog pin!

        :type name: str
        :param name:

        :type type: str
        :param type: Which type the sensor should check for. Can be: dry, moist or water

        :type debug: bool
        :param debug:
        """
        print_debug(debug, currentframe().f_code.co_name, 'Init moisture for: %s' % name)

        self.gpio = gpio
        self.uuid = uuid
        self.pin = pin
        self.analog_pin = analogPins.get(pin)
        self.name = name
        self.debug = debug
        self.__type = type

        self.min_threshold = self.DRY_MIN
        self.max_threshold = self.DRY_MAX
        if type == self.HUMID:
            self.min_threshold = self.HUMID_MIN
            self.max_threshold = self.HUMID_MAX
        elif type == self.WATER:
            self.min_threshold = self.WATER_MIN
            self.max_threshold = self.WATER_MAX

        all_params_str = u'UUID: {uuid}. Pin: {pin}. Name: {name}. Type: {type}. ' \
                         u'Min thresh: {min_thresh}. Max thresh: {max_thresh}'.format(
                            uuid=uuid,
                            pin=pin,
                            name=name,
                            type=type,
                            min_thresh=self.min_threshold,
                            max_thresh=self.max_threshold
                         )
        print_debug(debug, currentframe().f_code.co_name, all_params_str)


        self.gpio.pinMode(self.analog_pin, self.gpio.ANALOG_INPUT)

    def has_exceeded_threshold(self):
        return self.get_raw_read() > self.max_threshold

    def has_deceeded_threshold(self):
        return self.get_raw_read() < self.min_threshold

    def get_raw_read(self):
        try:
            raw = self.gpio.analogRead(self.analog_pin)
        except KeyError:
            raw = 100
            print 'Could not read pin: {analog_pin}. Is the moisture sensor really connected to that analog pin?' \
                .format(analog_pin=self.pin)
        print_debug(self.debug, currentframe().f_code.co_name, 'Raw read: ' + str(raw))
        return raw
