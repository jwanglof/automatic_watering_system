#!/usr/bin/env python
# coding=utf-8


class Moisture:

    def __init__(self, gpio, uuid, pin, name, debug=False):
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

        :type debug: bool
        :param debug:
        """
        self.gpio = gpio
        self.uuid = uuid
        self.pin = pin
        self.name = name
        self.debug = debug
