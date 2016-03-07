#!/usr/bin/env python
# coding=utf-8
from utils.AutomaticWateringSystem import AutomaticWateringSystem


class MagneticValue(AutomaticWateringSystem):
    """
    Simple class that helps to open and close a magnetic valve
    One instance represents one valve

    The relay that is used: http://www.seeedstudio.com/wiki/Grove_-_Relay
                            http://www.seeedstudio.com/depot/Grove-Relay-p-769.html
    """

    opened = 'OPENED'
    closed = 'CLOSED'

    def __init__(self, pin, name, debug=False):
        AutomaticWateringSystem.__init__(self, debug)

        self.name = name

        # Set the relay to output
        self.relay = self.gpio.pinMode(pin, self.gpio.OUTPUT)

        self.pin = pin

        self.status = self.closed

        self.is_added_to_queue = False

    def open_valve(self):
        self.status = self.opened
        self.gpio.digitalWrite(self.pin, self.gpio.HIGH)

    def close_valve(self):
        self.status = self.closed
        self.gpio.digitalWrite(self.pin, self.gpio.LOW)

    def get_status(self):
        return self.status

    def get_name(self):
        return self.name
