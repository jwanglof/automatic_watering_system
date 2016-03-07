#!/usr/bin/env python
# coding=utf-8
from datetime import datetime


def print_debug(debug, func_name, text):
    if debug:
        now = datetime.now().strftime("%B %d %I:%M:%S")
        print '{0} {1: <20}{2}'.format(now, func_name + ':', text)
