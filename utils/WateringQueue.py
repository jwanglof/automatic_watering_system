#!/usr/bin/env python
# coding=utf-8
from inspect import currentframe

from utils.MagneticValve import MagneticValue
from utils.print_debug import print_debug


class WateringQueue:
    """
    Implements a simple queue that holds which valve that should be opened next
    """
    def __init__(self, debug):
        """
        :type debug: bool
        :param debug:
        """
        self.debug = debug
        self.queue = []  # type: list[MagneticValue]
        self.current_valve = None  # type: MagneticValue

    def add_valve(self, valve):
        """
        :type valve: MagneticValue
        :param valve:
        :return:
        """
        print_debug(self.debug, currentframe().f_code.co_name, 'Adding valve with name: ' + valve.get_name())
        valve.is_added_to_queue = True
        self.queue.append(valve)

    def open_next(self):
        """
        Opens the next valve that is in the queue

        :raises IndexError: When the queue is empty
        """
        if self.current_valve is None:
            try:
                self.current_valve = self.queue.pop(0)
                self.current_valve.open_valve()
                print_debug(self.debug, currentframe().f_code.co_name, 'Opening: ' + self.current_valve.get_name())
            except IndexError as e:
                print_debug(self.debug, currentframe().f_code.co_name, 'No more valves in the queue!')
                raise

    def close_current(self):
        """
        Closes the current valve that is opened

        :raises IndexError: When there isn't a valve to close
        """
        if self.current_valve is not None:
            print_debug(self.debug, currentframe().f_code.co_name, 'Closing: ' + self.current_valve.get_name())
            self.current_valve.close_valve()
            self.current_valve.is_added_to_queue = False
            self.current_valve = None
            # Open the next in the queue
            self.open_next()
        else:
            print_debug(self.debug, currentframe().f_code.co_name, 'Can\'t close valve, no valve is open!')
            raise IndexError
