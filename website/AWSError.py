#!/usr/bin/env python
# coding=utf-8
from flask import render_template


class AWSError(Exception):
    default_error_message = 'Default error message, much useless, very ungood...'

    def __init__(self, message=default_error_message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

    def get_template(self):
        error_page = 'general'
        if self.status_code == 404:
            error_page = '404'

        return render_template('error_pages/{error_page}.html'.format(error_page=error_page),
                               error=self.to_dict()['message'],
                               status_code=self.status_code)
