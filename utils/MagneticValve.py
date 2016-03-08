#!/usr/bin/env python
# coding=utf-8


# class MagneticValve(AutomaticWateringSystem):
from inspect import currentframe
from threading import Timer

from blinker import signal

from utils import blinker_signals
from utils.print_debug import print_debug


class MagneticValve:
    """
    Simple class that helps to open and close a magnetic valve
    One instance represents one valve

    The relay that is used: http://www.seeedstudio.com/wiki/Grove_-_Relay
                            http://www.seeedstudio.com/depot/Grove-Relay-p-769.html
    """

    opened = 'OPENED'
    closed = 'CLOSED'

    def __init__(self, gpio, uuid, pin, name, debug=False):
        """
        Constructor

        :type gpio: GPIOGalileoGen2
        :param gpio: An instance of GPIOGalileoGen2

        :type uuid: uuid4
        :param uuid: Unique identifier the parent class created

        :type pin: int
        :param pin: Which pin the magnetic valve is connected to

        :type name: str
        :param name:

        :type debug: bool
        :param debug:
        """
        print_debug(debug, currentframe().f_code.co_name, 'Init %s' % name)
        # AutomaticWateringSystem.__init__(self, debug)

        self.gpio = gpio
        self.__uuid = uuid
        self.pin = pin
        self.__name = name
        self.debug = debug

        # Set the relay to output
        self.gpio.pinMode(pin, self.gpio.OUTPUT)

        self.__status = self.closed

        self.is_added_to_queue = False

        self.open_valve_signal = signal(blinker_signals['open_valve'])
        self.close_valve_signal = signal(blinker_signals['close_valve'])

    def send_open_valve_signal(self):
        """
        Send the open-valve-event
        """
        print_debug(self.debug, currentframe().f_code.co_name, 'Opening event %s' % self.__name)
        self.open_valve_signal.send(self)

    def open_valve(self):
        print_debug(self.debug, currentframe().f_code.co_name, 'Opening %s' % self.__name)

        self.__status = self.opened
        self.gpio.digitalWrite(self.pin, self.gpio.HIGH)

        timer_time = 0.5
        if self.debug:
            timer_time = 5
        timer = Timer(timer_time, self.close_valve)
        timer.start()
        # s = scheduler(time, sleep)
        # s.enter(timer_time, 1, self.close_valve, '')
        # s.run()

    def close_valve(self):
        print_debug(self.debug, currentframe().f_code.co_name, 'Closing %s' % self.__name)
        # Send the close-valve-event
        self.close_valve_signal.send(self)
        self.__status = self.closed
        self.gpio.digitalWrite(self.pin, self.gpio.LOW)

    @property
    def get_name(self):
        return self.__name

    @property
    def get_uuid(self):
        return self.__uuid

    @property
    def get_status(self):
        return self.__status
