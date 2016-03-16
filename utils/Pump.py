#!/usr/bin/env python
# coding=utf-8
from inspect import currentframe
from threading import Timer

from blinker import signal
from wiringx86 import GPIOGalileoGen2 as GPIO

from utils import blinker_signals
from utils.pins import digitalPins
from utils.print_debug import print_debug

from AWS.MagneticValve import MagneticValve


class Pump:
    """
    Simple class that helps to open and close a pump that is connected to the board
    One instance represents one pump
    """

    opened = 'OPENED'
    closed = 'CLOSED'

    def __init__(self, pin, name, debug=False, gpio_debug=False):
        print_debug(debug, currentframe().f_code.co_name, 'Init pump: %s' % name, __name__)

        self.pin = pin
        self.name = name
        self.digital_pin = digitalPins.get(pin)
        self.debug = debug

        all_params_str = u'Pin: {pin}. Name: {name}'.format(
            pin=pin,
            name=name,
        )
        print_debug(debug, currentframe().f_code.co_name, all_params_str, __name__)

        # Get a new instance of the GPIO
        self.gpio = GPIO(debug=gpio_debug)  # type: GPIO

        # Set the pump to output
        self.gpio.pinMode(pin, self.gpio.OUTPUT)

        # Set the pumps initial status to closed
        self.__status = self.closed

        # Events the pump can send
        self.pump_is_turned_on = signal(blinker_signals['pump_is_on'])
        self.pump_is_turned_off = signal(blinker_signals['pump_is_off'])

    def turn_on_pump(self, magnetic_valve):
        """
        Will open a specific pump and when it's open, and filled with water, it will open the valve provided

        :type magnetic_valve: MagneticValve
        :param magnetic_valve: The valve that should be opened while the pump is opened
        """
        print_debug(self.debug, currentframe().f_code.co_name, 'Turning on pump: %s' % self.name, __name__)
        self.__status = self.opened
        self.gpio.digitalWrite(self.digital_pin, self.gpio.HIGH)

        # Open the valve after 1 second so we know there's water in the hose
        timer_time = 1
        timer = Timer(timer_time, self.__send_turned_on_event, args=[magnetic_valve])
        timer.start()

    def turn_off_pump(self):
        """
        Turn off the pump
        :return:
        """
        print_debug(self.debug, currentframe().f_code.co_name, 'Turning off pump: %s' % self.name, __name__)
        self.__status = self.closed
        self.gpio.digitalWrite(self.digital_pin, self.gpio.LOW)

    def cleanup(self):
        """
        Turn off the pump on cleanup
        """
        self.turn_off_pump()

    def __send_turned_on_event(self, valve):
        """
        Send the turn on signal to the WateringQueue so it knows that it can open the valve
        :param valve:
        :return:
        """
        self.pump_is_turned_on.send(valve)

    @property
    def is_opened(self):
        return self.__status is self.opened
