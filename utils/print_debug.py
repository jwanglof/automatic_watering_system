#!/usr/bin/env python
# coding=utf-8
from datetime import datetime


def print_debug(debug, func_name, text, class_name=None):
    if debug:
        now = datetime.now().strftime("%B %d %I:%M:%S")
        if class_name is not None:
            print u'{0} {1: <60}{2}'.format(now, func_name + ' (' + class_name + '):', text).encode('utf-8')
        else:
            print u'{0} {1: <60}{2}'.format(now, func_name + ':', text).encode('utf-8')
