#!/usr/bin/env python
# coding=utf-8

voltage_resolution = 1023.0


def from_voltage(voltage):
    """
    Convert voltage to a percent value
    1023 will return 1
    511,5 will return 0.5
    :param voltage:
    :return:
    """
    return voltage / voltage_resolution


def to_voltage(percent):
    """
    Convert the percent to voltage
    1 will return 1023
    0.5 will return 511,5
    :param percent:
    :return:
    """
    return percent * voltage_resolution
