#!/usr/bin/env python
# coding=utf-8
from time import time

from flask.ext.wtf import Form
from wtforms import validators, StringField, IntegerField, SelectField


class PumpForm(Form):
    created = IntegerField(label='created', default=time())
    name = StringField(label='Name *',
                       description='Specify a name to make it easier to find it for you',
                       validators=[
                           validators.DataRequired('You must apply a name for the pump. '
                                                   'This will make it easier to find it later')
                       ])
    pin = IntegerField(label='Pin *',
                       description='Specify which pin the pump is added to',
                       validators=[
                           validators.DataRequired('You must apply which pin the pump is attached to!')
                       ])
    pin_type = SelectField(label='Pin type *',
                           description='Specify which pin-type the pump is hooked up to',
                           choices=[('analog', 'Analog'), ('digital', 'Digital'), ('pwm', 'PWM')],
                           validators=[
                               validators.DataRequired('You must specify what pin-type the pump is attached to '
                                                       '(analog, digital, pwm)')
                           ])
    location = StringField(label='Location',
                           description='Specify the location of the pump so it\'s easier to find it',
                           validators=[
                               validators.Optional()
                           ])
    description = StringField(label='Description',
                              description='Add a small description of the pump; is it white, '
                                          'does it make a lot of noise?',
                              validators=[
                                  validators.Optional()
                              ])
