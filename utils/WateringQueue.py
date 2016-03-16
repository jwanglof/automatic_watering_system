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
    def __init__(self, debug, pumps):
        """
        :type debug: bool
        :param debug:
        """
        self.debug = debug
        self.pumps = pumps
        self.queue = []  # type: list[MagneticValve]
        self.current_opened_valve = None  # type: MagneticValve

        # Event receivers
        open_valve_receiver = signal(blinker_signals['open_valve'])
        open_valve_receiver.connect(self.open_or_queue_valve)
        close_valve_receiver = signal(blinker_signals['close_valve'])
        close_valve_receiver.connect(self.close_valve_event)

        opened_pump_receiver = signal(blinker_signals['pump_is_on'])
        opened_pump_receiver.connect(self.__open_current)

    def add_valve_to_queue(self, valve):
        """
        :type valve: MagneticValve
        :param valve:
        """
        # Check that the valve isn't already in the queue
        if not self.is_valve_in_queue(valve):
            print_debug(self.debug, currentframe().f_code.co_name, 'Adding valve to queue: ' + valve.get_name, __name__)
            valve.is_added_to_queue = True
            self.queue.append(valve)
        else:
            print_debug(self.debug, currentframe().f_code.co_name,
                        'Will not add "{name}" to queue, already in the queue!'.format(name=valve.get_name), __name__)

    def is_valve_in_queue(self, valve):
        """
        :type valve: MagneticValve
        :param valve:
        :rtype: bool
        :return: If the valve is in the queue or not
        """
        return any(v.get_uuid is valve.get_uuid for v in self.queue)

    def open_or_queue_valve(self, valve):
        """
        Opens a valve if no other valve are opened, else it will be added to the queue
        :type valve: MagneticValve
        """
        if isinstance(valve, MagneticValve):
            print_debug(self.debug, currentframe().f_code.co_name,
                        'Got opening event from valve: {name}'.format(name=valve.get_name), __name__)

            # Open the valve if no valve is opened
            # Else, add the valve to the queue
            if self.current_opened_valve is None:
                print_debug(self.debug, currentframe().f_code.co_name,
                            'Will open valve: {name}'.format(name=valve.get_name), __name__)

                # Open the plant's pump before we open any valves!
                # If the pump is open we will just open the valve, else we must wait for the open-event
                pump = self.pumps.get(valve.get_pump_id)
                if not pump.is_opened:
                    pump.turn_on_pump(valve)
                else:
                    self.__open_current(valve)

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
                    'Valve has been closed: {name}'.format(name=valve.get_name), __name__)

        if self.current_opened_valve.get_uuid is valve.get_uuid:
            print_debug(self.debug, currentframe().f_code.co_name,
                        'Valve was the opened valve: {name}'.format(name=valve.get_name), __name__)
            self.current_opened_valve = None

            # Turn off the active pump
            # TODO This should not be done immediately, should check if the queue is empty or not, and if it isn't empty we should check that if any plants in the queue have the same pump. If this exist, we should leave the pump open!
            pump = self.pumps.get(valve.get_pump_id)
            pump.turn_off_pump()

            self.__open_next()
        else:
            print_debug(self.debug, currentframe().f_code.co_name,
                        'The closed valve was NOT the one opened! Name: {name}'.format(name=valve.get_name), __name__)
            # raise RuntimeError

    def __open_next(self):
        """
        Open the next valve in the queue
        """
        if len(self.queue) > 0:
            print_debug(self.debug, currentframe().f_code.co_name,
                        'Will open the next valve in queue', __name__)

            self.open_or_queue_valve(self.queue[0])
        else:
            print_debug(self.debug, currentframe().f_code.co_name,
                        'No more valves in the queue!', __name__)

            # raise IndexError

    def __remove_from_queue(self, valve):
        """
        Remove the valve from the queue
        :type valve: MagneticValve
        :param valve: The valve to remove
        """
        print_debug(self.debug, currentframe().f_code.co_name,
                    'Removing from queue: {name}'.format(name=valve.get_name), __name__)

        self.queue.remove(valve)

    def __open_current(self, valve):
        """
        This function will actually open the valve
        :type valve: MagneticValve
        :param valve: Specifies which valve to open
        """
        print_debug(self.debug, currentframe().f_code.co_name,
                    'Opening valve: {name}'.format(name=valve.get_name), __name__)

        self.current_opened_valve = valve

        # Remove the valve from the queue if it exist so it can be re-added
        if valve.is_added_to_queue:
            self.__remove_from_queue(valve)

        # Open the valve
        valve.open_valve()
