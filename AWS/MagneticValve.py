#!/usr/bin/env python
# coding=utf-8


# class MagneticValve(AutomaticWateringSystem):
from inspect import currentframe
from threading import Timer

from blinker import signal

from utils import blinker_signals
from utils.pins import digitalPins
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

    def __init__(self, gpio, uuid, pin, name, pump_id, open_time=0.5, debug=False):
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

        :type open_time: float
        :param open_time: Specify how long the valve should be open

        :type debug: bool
        :param debug:
        """
        print_debug(debug, currentframe().f_code.co_name, 'Init %s' % name, __name__)
        all_params_str = u'UUID: {uuid}. Pin: {pin}. Name: {name}. Pump ID: {pump_id}, Open time: {open_time}'.format(
            uuid=uuid,
            pin=pin,
            name=name,
            pump_id=pump_id,
            open_time=open_time
        )
        print_debug(debug, currentframe().f_code.co_name, all_params_str)

        self.gpio = gpio
        self.__uuid = uuid
        self.pin = pin
        self.digital_pin = digitalPins.get(pin)
        self.__name = name
        self.__pump_id = pump_id
        self.__open_time = open_time
        self.debug = debug

        # Set the relay to output
        self.gpio.pinMode(pin, self.gpio.OUTPUT)

        # Set the initial status to closed
        self.__status = self.closed

        self.is_added_to_queue = False

        # Events the valve can send
        self.open_valve_signal = signal(blinker_signals['open_valve'])
        self.close_valve_signal = signal(blinker_signals['close_valve'])
        self.valve_removed_signal = signal(blinker_signals['removed_valve'])

    def send_open_valve_signal(self):
        """
        Send the open-valve-event
        """
        print_debug(self.debug, currentframe().f_code.co_name, 'Opening event %s' % self.__name, __name__)
        self.open_valve_signal.send(self)

    def open_valve(self):
        """
        Open the valve and close it after the specified open_time
        """
        print_debug(self.debug, currentframe().f_code.co_name, 'Opening %s' % self.__name, __name__)

        self.__status = self.opened
        self.gpio.digitalWrite(self.digital_pin, self.gpio.HIGH)

        timer = Timer(self.__open_time, self.close_valve)
        timer.start()

    def close_valve(self):
        """
        Closes the valve and will send the close-event for the WateringQueue
        """
        print_debug(self.debug, currentframe().f_code.co_name, 'Closing %s' % self.__name, __name__)
        # Send the close-valve-event
        self.close_valve_signal.send(self)
        self.__status = self.closed
        self.gpio.digitalWrite(self.digital_pin, self.gpio.LOW)

    def cleanup(self):
        """
        Close the valve when cleaning up
        """
        self.valve_removed_signal.send(self)

    @property
    def get_name(self):
        return self.__name

    @property
    def get_uuid(self):
        return self.__uuid

    @property
    def get_status(self):
        return self.__status

    @property
    def get_pump_id(self):
        return self.__pump_id

    @property
    def is_opened(self):
        return self.__status == self.opened

    @property
    def is_closed(self):
        return self.__status == self.closed
