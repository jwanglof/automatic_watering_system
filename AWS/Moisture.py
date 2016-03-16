#!/usr/bin/env python
# coding=utf-8
from inspect import currentframe

from utils.pins import analogPins
from utils.print_debug import print_debug


# TODO Setter for the threshold if the user wants to change them!

class Moisture:
    """
    http://seeedstudio.com/wiki/Grove_-_Moisture_Sensor

    TODO:
    Raw values:
        WET: >= 600
        DAMP: 360 <> 600
        DRY: <= 350

    Percent values:
        WET: >= 100%
        DAMP: 60% <> 100%
        DRY: <= 60%

    100% = 600 (can go higher!)
    1% = 6
    """

    DRY = 'dry'
    DRY_MIN = 0
    DRY_MAX = 350
    DRY_MIN_PERCENT = 0
    DRY_MAX_PERCENT = 60
    HUMID = 'humid'
    HUMID_MIN = 360
    HUMID_MAX = 600
    HUMID_MIN_PERCENT = 60
    HUMID_MAX_PERCENT = 100
    WATER = 'water'
    WATER_MIN = 600
    WATER_MAX = 1400
    WATER_MIN_PERCENT = 100

    def __init__(self, gpio, uuid, pin, name, min_percent, max_percent, debug=False):
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

        :type min_percent: int
        :param min_percent: Specify the minimum threshold for the moisture

        :type max_percent: int
        :param max_percent: Specify the minimum threshold for the moisture

        :type debug: bool
        :param debug:
        """
        print_debug(debug, currentframe().f_code.co_name, 'Init moisture for: %s' % name, __name__)

        self.gpio = gpio
        self.uuid = uuid
        self.pin = pin
        self.analog_pin = analogPins.get(pin)
        self.name = name
        self.debug = debug

        self.min_percent = min_percent
        self.max_percent = max_percent

        all_params_str = u'UUID: {uuid}. Pin: {pin}. Name: {name}. Min percent: {min_percent}. ' \
                         u'Max percent: {max_percent}'.format(
                            uuid=uuid,
                            pin=pin,
                            name=name,
                            type=type,
                            min_percent=min_percent,
                            max_percent=max_percent
                         )
        print_debug(debug, currentframe().f_code.co_name, all_params_str, __name__)

        self.gpio.pinMode(self.analog_pin, self.gpio.ANALOG_INPUT)

    def has_exceeded_threshold(self):
        """
        :rtype: bool
        :return: Check if the sensor is below the specified maximum threshold
        """
        return self.get_percent_read() > self.max_percent

    def has_deceeded_threshold(self):
        """
        :rtype: bool
        :return: Check if the sensor is below the specified minimum threshold
        """
        return self.get_percent_read() < self.min_percent

    def get_raw_read(self):
        """
        :rtype: int
        :return: The raw value from the sensor
        """
        try:
            raw = self.gpio.analogRead(self.analog_pin)
        except KeyError:
            raw = 100
            print 'Could not read pin: {analog_pin}. Is the moisture sensor really connected to that analog pin?' \
                .format(analog_pin=self.pin)
        print_debug(self.debug, currentframe().f_code.co_name, 'Raw read: ' + str(raw), __name__)
        return raw

    def get_percent_read(self):
        """
        Equation: Y = P% * X

        Solving our equation for P
        Y = raw_value
        X = WATER_MIN
        P% = Y/X

        Example:
            P% = 650/600
            p = 1.0833

        :rtype: float
        :return: The percent the raw value is right now
        """
        percent = (float(self.get_raw_read()) / float(self.WATER_MIN)) * 100
        print_debug(self.debug, currentframe().f_code.co_name, 'Percent read: ' + str(percent), __name__)
        return percent

    @staticmethod
    def cleanup():
        """
        Don't really need any clean-up since the pin is analog
        """
        pass
