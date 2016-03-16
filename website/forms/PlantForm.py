#!/usr/bin/env python
# coding=utf-8
from time import time

from wtforms import validators, StringField, IntegerField, SelectField
from wtforms_custom_validators.GreaterThanOrEqual import GreaterThanOrEqual
from flask.ext.wtf import Form

percent_choices = [
    (0, '0%'),
    (10, '10%'),
    (20, '20%'),
    (30, '30%'),
    (40, '40%'),
    (50, '50%'),
    (60, '60%'),
    (70, '70%'),
    (80, '80%'),
    (90, '90%'),
    (100, '100%')
]


class PlantForm(Form):
    created = IntegerField(label='created', default=time())
    name = StringField(label='Name *',
                       description='Well, obviously the plant needs to have a name so you can find it later '
                                   'when you\'re adding your own plants!',
                       validators=[
                           validators.DataRequired('Must supply a name')
                       ])

    min_moisture = SelectField(label='Min moisture *',
                               coerce=int,
                               description='Specify the plants threshold for its minimum moisture. '
                                           '0% is completely dry, 100% is water',
                               choices=percent_choices,
                               default=60,
                               validators=[
                                   validators.DataRequired('You must specify how dry the dirt can be')
                               ])
    max_moisture = SelectField(label='Max moisture *',
                               coerce=int,
                               description='Specify the plants threshold for its maximum moisture. '
                                           '0% is completely dry, 100% is water',
                               choices=percent_choices,
                               default=80,
                               validators=[
                                   validators.DataRequired('You must specify how wet the dirt can be'),
                                   GreaterThanOrEqual('min_moisture',
                                                      'Max moisture must be smaller than min moisture!')
                               ])

    max_temperature = IntegerField(label='Max temperature',
                                   description='Specify the plants threshold for its maximum temperature. '
                                               'Specify temperature in celsius!',
                                   validators=[
                                       validators.Optional()
                                   ])
    min_temperature = IntegerField(label='Min temperature',
                                   description='Specify the plants threshold for its minimum temperature. '
                                               'Specify temperature in celsius!',
                                   validators=[
                                       validators.Optional()
                                   ])

    # moisture = SelectField(label='Pin type *',
    #                        description='Specify what kind of soil you the plant need',
    #                        choices=[('dry', 'Dry soil'), ('humid', 'Humid soil'), ('water', 'Water')],
    #                        validators=[
    #                            validators.DataRequired('You must specify what kind of soil the plant need')
    #                        ])
    # max_moisture = IntegerField(label='Max moisture',
    #                             description='Specify the plants threshold for its maximum moisture',
    #                             validators=[
    #                                 validators.Optional()
    #                             ])
    # min_moisture = IntegerField(label='Min moisture',
    #                             description='Specify the plants threshold for its minimum moisture',
    #                             validators=[
    #                                 validators.Optional()
    #                             ])
