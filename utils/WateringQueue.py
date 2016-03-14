#!/usr/bin/env python
# coding=utf-8
from inspect import currentframe

from blinker import signal

from AWS.MagneticValve import MagneticValve
from utils import blinker_signals
from utils.print_debug import print_debug


class WateringQueue:
    """
    Implements a simple queue that holds which valve that should be opened next
    This class makes sure that only one valve is opened at any time
    """
    def __init__(self, debug):
        """
        :type debug: bool
        :param debug:
        """
        self.debug = debug
        self.queue = []  # type: list[MagneticValve]
        self.current_opened_valve = None  # type: MagneticValve

        # Event receivers
        open_valve_receiver = signal(blinker_signals['open_valve'])
        open_valve_receiver.connect(self.open_or_queue_valve)
        close_valve_receiver = signal(blinker_signals['close_valve'])
        close_valve_receiver.connect(self.close_valve_event)

    def add_valve_to_queue(self, valve):
        """
        :type valve: MagneticValve
        :param valve:
        :return:
        """
        # Check that the valve isn't already in the queue
        if not self.is_valve_in_queue(valve):
            print_debug(self.debug, currentframe().f_code.co_name, 'Adding valve to queue: ' + valve.get_name)
            valve.is_added_to_queue = True
            self.queue.append(valve)
        else:
            print_debug(self.debug, currentframe().f_code.co_name,
                        'Will not add "{name}" to queue, already in the queue!'.format(name=valve.get_name))

    def is_valve_in_queue(self, valve):
        return any(v.get_uuid is valve.get_uuid for v in self.queue)

    def open_or_queue_valve(self, valve):
        """
        Opens a valve if no other valve are opened, else it will be added to the queue
        :type valve: MagneticValve
        """
        if isinstance(valve, MagneticValve):
            print_debug(self.debug, currentframe().f_code.co_name,
                        'Got opening event from valve: {name}'.format(name=valve.get_name))

            # Open the valve if no valve is opened
            # Else, add the valve to the queue
            if self.current_opened_valve is None:
                print_debug(self.debug, currentframe().f_code.co_name,
                            'Opening valve: {name}'.format(name=valve.get_name))

                # Remove the valve from the queue if it exist
                if valve.is_added_to_queue:
                    self.__remove_from_queue(valve)

                self.current_opened_valve = valve

                # Open the valve
                valve.open_valve()
            else:
                self.add_valve_to_queue(valve)
        else:
            error = ReferenceError
            error.message = 'valve needs to be of the type MagneticValve!'
            raise error

    def close_valve_event(self, valve):
        """
        Listens to the close-valve-event.
        When a valve is closed this function will open the next valve in the queue if the closed valve
         was the one that was opened
        :type valve: MagneticValve
        :param valve:
        """
        print_debug(self.debug, currentframe().f_code.co_name,
                    'Valve has been closed: {name}'.format(name=valve.get_name))

        if self.current_opened_valve.get_uuid is valve.get_uuid:
            print_debug(self.debug, currentframe().f_code.co_name,
                        'Valve was the opened valve: {name}'.format(name=valve.get_name))
            self.current_opened_valve = None
            self.__open_next()
        else:
            print_debug(self.debug, currentframe().f_code.co_name,
                        'The closed valve was NOT the one opened! Name: {name}'.format(name=valve.get_name))
            # raise RuntimeError

    def __open_next(self):
        if len(self.queue) > 0:
            print_debug(self.debug, currentframe().f_code.co_name,
                        'Will open the next valve in queue')

            self.open_or_queue_valve(self.queue[0])
        else:
            print_debug(self.debug, currentframe().f_code.co_name,
                        'No more valves in the queue!')

            # raise IndexError

    def __remove_from_queue(self, valve):
        print_debug(self.debug, currentframe().f_code.co_name,
                    'Removing from queue: {name}'.format(name=valve.get_name))

        self.queue.remove(valve)
