#!/usr/bin/env python
# coding=utf-8
import time
from wiringx86 import GPIOGalileoGen2 as GPIO

from utils import Temperature, Database
from utils.pins import analogPins, digitalPins

from utils.MagneticValve import MagneticValue
from utils.WateringQueue import WateringQueue

# TODO
# Kan ha en kö med vilka växter som ska vattnas. En växt vattnas åt gången. Då spelar huvudslangens diameter ingen roll!
# Om det inte rinner något vatten ska summern låta (måste ha en Grove som kollar vattenflödet då!)
# ?? Borde implementera någon kö som har alla sensorer i sig som kollar varje minut (?).
#    Ska klasserna pusha in sig själva varje minut till en kö som väntar på att en klass blir klar, och sen kör nästa?

gpio = GPIO(debug=True)
#
# buzzer_pin = digitalPins.get(8)
# gpio.pinMode(buzzer_pin, gpio.OUTPUT)
#
# led_pin = digitalPins.get(6)
# gpio.pinMode(led_pin, gpio.OUTPUT)

# servo_pin = analogPins.get(2)
# gpio.pinMode(servo_pin, gpio.PWM)
# gpio.setPWMPeriod(servo_pin, 1500)

if __name__ == '__main__':
    # NOTE: There will exist one class PER temperature sensor
    temperature_pin = 0
    GetTemperature = Temperature(analogPins.get(temperature_pin), 30)

    # NOTE: There will exist one class PER magnetic valve
    magnetic_valve_pin = 6
    ChiliMagneticValve = MagneticValue(digitalPins.get(magnetic_valve_pin), 'CHILI #1', True)

    buzzer_pin = 3
    FlowerMagneticValve = MagneticValue(digitalPins.get(buzzer_pin), 'FLOWER #1', True)

    ValveQueue = WateringQueue(True)

    # database = Database()

    try:
        while True:
            # temp = GetTemperature.get_celsius()
            # database.add_statistic(temperature=temp)
            print 'Exceeded: ' + str(GetTemperature.has_exceeded_threshold())
            print 'Temp: ' + str(GetTemperature.get_celsius())
            print 'Added: ' + str(ChiliMagneticValve.is_added_to_queue)
            print 'Added 2: ' + str(FlowerMagneticValve.is_added_to_queue)

            try:
                if GetTemperature.has_exceeded_threshold() and not ChiliMagneticValve.is_added_to_queue:
                    # gpio.digitalWrite(buzzerPin, gpio.HIGH)
                    # gpio.digitalWrite(led_pin, gpio.HIGH)
                    ValveQueue.add_valve(ChiliMagneticValve)
                    ValveQueue.open_next()
                elif not GetTemperature.has_exceeded_threshold() and ChiliMagneticValve.is_added_to_queue:
                    # gpio.digitalWrite(buzzerPin, gpio.LOW)
                    # gpio.digitalWrite(led_pin, gpio.LOW)
                    ValveQueue.close_current()
            except IndexError as e:
                print e

            try:
                if GetTemperature.has_exceeded_threshold() and not FlowerMagneticValve.is_added_to_queue:
                    # gpio.digitalWrite(buzzerPin, gpio.HIGH)
                    # gpio.digitalWrite(led_pin, gpio.HIGH)
                    ValveQueue.add_valve(FlowerMagneticValve)
                    ValveQueue.open_next()
                elif not GetTemperature.has_exceeded_threshold() and FlowerMagneticValve.is_added_to_queue:
                    # gpio.digitalWrite(buzzerPin, gpio.LOW)
                    # gpio.digitalWrite(led_pin, gpio.LOW)
                    ValveQueue.close_current()
            except IndexError as e:
                print e

            time.sleep(1)
    except KeyboardInterrupt:
        GetTemperature.gpio.cleanup()


# # pin = 13
# # analogpin = 14
# pin = pins.ledPin
# analogpin = pins.analogPins.get(1)
#
# print 'Setting up all pins...'
#
# # Set pin 14 to be used as an analog input GPIO pin.
# gpio.pinMode(analogpin, gpio.ANALOG_INPUT)
#
# # Set pin 13 to be used as an output GPIO pin.
# gpio.pinMode(pin, gpio.OUTPUT)
#
# print 'Analog reading from pin %d now...' % analogpin
# try:
#     while(True):
#         # Read the voltage on pin 14
#         value = gpio.analogRead(analogpin)
#
#         print value
#         print convertVoltage.from_voltage(value)
#
#         # Turn ON pin 13
#         gpio.digitalWrite(pin, gpio.HIGH)
#
#         # Sleep for a while depending on the voltage we just read. The higher
#         # the voltage the more we sleep.
#         time.sleep(convertVoltage.from_voltage(value))
#
#         # Turn OFF pin 13
#         gpio.digitalWrite(pin, gpio.LOW)
#
#         # Sleep for a while depending on the voltage we just read. The higher
#         # the voltage the more we sleep.
#         time.sleep(convertVoltage.from_voltage(value))
#
# # When you get tired of seeing the led blinking kill the loop with Ctrl-C.
# except KeyboardInterrupt:
#     # Leave the led turned off.
#     print '\nCleaning up...'
#     gpio.digitalWrite(pin, gpio.LOW)
#
#     # Do a general cleanup. Calling this function is not mandatory.
#     gpio.cleanup()

##########

# pin = constants.ledPin
# state = gpio.HIGH
#
# # Set pin 13 to be used as an output GPIO pin.
# print 'Setting up pin %d' % pin
# gpio.pinMode(pin, gpio.OUTPUT)
#
# print 'Blinking pin %d now...' % pin
# try:
#     while(True):
#         # Write a state to the pin. ON or OFF.
#         gpio.digitalWrite(pin, state)
#
#         # Toggle the state.
#         state = gpio.LOW if state == gpio.HIGH else gpio.HIGH
#
#         # Sleep for a while.
#         sleep(0.5)
#
# # When you get tired of seeing the led blinking kill the loop with Ctrl-C.
# except KeyboardInterrupt:
#     # Leave the led turned off.
#     print '\nCleaning up...'
#     gpio.digitalWrite(pin, gpio.LOW)
#
#     # Do a general cleanup. Calling this function is not mandatory.
#     gpio.cleanup()
#
# def run():
#
#

