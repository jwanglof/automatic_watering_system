#!/usr/bin/env python
# coding=utf-8
from time import time

from flask.ext.wtf import Form
from wtforms import validators, StringField, IntegerField, SelectField


class OwnPlantForm(Form):
    created = IntegerField(label='created', default=time())
    plant_id = SelectField(label='Plant ID *', #coerce=int,
                           description='Needed to know which threshold the plant have',
                           validators=[
                               validators.DataRequired('You must apply which plant this entry is for!')
                           ])
    pump_id = SelectField(label='Pump ID *',
                          description='Needed so we know which pump to turn on/off',
                          validators=[
                              validators.DataRequired('You must choose which pump the plant is connected to!')
                          ])
    name = StringField(label='Name *',
                       description='To supply a name for the plant makes it easier for you to find it',
                       validators=[
                           validators.DataRequired('You must specify a name for the plant. '
                                                   'This makes it easier for you, you\'re welcome!')
                       ])
    description = StringField(label='Description',
                              description='Add a description for this plant',
                              validators=[
                                  validators.Optional()#,
                                  # If(lambda form, field: form.plant_id.data, StringField())
                              ])
    magnetic_valve_pin = IntegerField(label='Magnetic valve pin *',
                                      description='Specify which pin on the board the magnetic valve is connected to. '
                                                  '<br /><u>This needs to be a digital pin!</u>',
                                      validators=[
                                          validators.DataRequired('You must specify which pin the magnetic '
                                                                  'valve is connected to!')
                                      ])
    moisture_sensor_pin = IntegerField(label='Moisture sensor pin',
                                       description='Specify which pin on the board the moisture sensor is connected to.'
                                                   '<br /><u>This must be an analog pin!</u>',
                                       validators=[
                                           validators.Optional()
                                       ])
    temperature_sensor_pin = IntegerField(label='Temperature sensor pin',
                                          description='Specify which pin on the board the temperature sensor is '
                                                      'connected to. <br /><u>This must be an analog pin!</u>',
                                          validators=[
                                              validators.Optional()
                                          ])
