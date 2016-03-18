#!/usr/bin/env python
# coding=utf-8
from inspect import currentframe

from blinker import signal

from AWS.MagneticValve import MagneticValve
from utils import blinker_signals
from utils.Pump import Pump
from utils.print_debug import print_debug

from utils.class_instances import pumps

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
        self.__current_opened_valve = None  # type: MagneticValve
        self.__current_opened_pump = None  # type: Pump

        # Event receivers
        open_valve_receiver = signal(blinker_signals['open_valve'])
        open_valve_receiver.connect(self.open_or_queue_valve)
        close_valve_receiver = signal(blinker_signals['close_valve'])
        close_valve_receiver.connect(self.close_valve_event)
        removed_valve_signal = signal(blinker_signals['removed_valve'])
        removed_valve_signal.connect(self.__remove_valve_and_close)

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
            if self.__current_opened_valve is None:
                print_debug(self.debug, currentframe().f_code.co_name,
                            'Will open valve: {name}'.format(name=valve.get_name), __name__)

                self.__current_opened_valve = valve

                # Open the plant's pump before we open any valves!
                # If the pump is open we will just open the valve, else we must wait for the open-event
                pump = pumps.get(valve.get_pump_id)
                self.__current_opened_pump = pump
                if not pump.is_opened:
                    pump.turn_on_pump(valve)
                else:
                    self.__open_current(valve)

            else:
                self.add_valve_to_queue(valve)
        else:
            error = TypeError
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

        # Make sure that we're trying to close the opened valve
        if self.__current_opened_valve.get_uuid == valve.get_uuid:
            print_debug(self.debug, currentframe().f_code.co_name,
                        'Current valve was the opened one: {name}'.format(name=valve.get_name), __name__)
            self.__current_opened_valve = None

            first_valve_in_queue = self.__get_first_in_queue()

            # Turn off the active pump if the next plant that is in the queue is using another pump
            if first_valve_in_queue is not None:
                if first_valve_in_queue.get_pump_id != self.__current_opened_pump.uuid:
                    to_pump = pumps.get(first_valve_in_queue.get_pump_id)  # type: Pump
                    print_str = 'Not the same pump, will switch! From pump: {from_pump_name}. To pump: {to_pump_name}.'\
                        .format(to_pump_name=to_pump.name, from_pump_name=self.__current_opened_pump.name)
                    self.__turn_off_pump(valve.get_pump_id)
                else:
                    print_str = 'The next plant have the same pump, will not turn off pump: {pump_name}!'\
                        .format(pump_name=self.__current_opened_pump.name)

                print_debug(self.debug, currentframe().f_code.co_name, print_str, __name__)
            else:
                # Turn off the current pump since no plants are in the queue
                print_debug(self.debug, currentframe().f_code.co_name,
                            'No more valves in queue, will turn of the current pump', __name__)
                self.__turn_off_pump()

            # Open the next valve in the queue
            self.__open_next()
        else:
            print_debug(self.debug, currentframe().f_code.co_name,
                        'The closed valve was NOT the one opened! Name: {name}'.format(name=valve.get_name), __name__)
            # raise RuntimeError

    def __remove_valve_and_close(self, valve):
        """
        Will be executed when the removed-valve-event is sent
        When this function runs it will check if the valve is in the queue and remove if it is is, and also
         close the valve if it is open

        :type valve: MagneticValve
        :param valve:
        """
        if self.is_valve_in_queue(valve):
            self.__remove_from_queue(valve)

        if valve.is_opened:
            if self.__current_opened_valve is not None and self.__current_opened_valve.get_uuid == valve.get_uuid:
                self.close_valve_event(valve)

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

    def __get_first_in_queue(self):
        """
        Get the first valve in the queue, or None if it's empty

        :rtype: MagneticValve
        :return:
        """
        if len(self.queue) > 0:
            return self.queue[0]
        return None

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

        # Remove the valve from the queue if it exist so it can be re-added
        if valve.is_added_to_queue:
            self.__remove_from_queue(valve)

        # Open the valve
        valve.open_valve()

    def __turn_off_pump(self, pump_id=None):
        """
        Turn off a specific pump
        If pump_id is None it will turn of the pump that currently is on

        :type pump_id: str
        :param pump_id:
        """
        if pump_id is None:
            pump_id = self.__current_opened_pump.uuid

        self.__current_opened_pump = None
        pump = pumps.get(pump_id)
        print_debug(self.debug, currentframe().f_code.co_name,
                    'Turning off pump: {name}'.format(name=pump.name), __name__)
        pump.turn_off_pump()
