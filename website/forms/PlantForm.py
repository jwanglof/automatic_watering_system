#!/usr/bin/env python
# coding=utf-8
from time import time

from wtforms import validators, StringField, IntegerField, SelectField
from flask.ext.wtf import Form


class PlantForm(Form):
    created = IntegerField(label='created', default=time())
    name = StringField(label='Name *',
                       description='Well, obviously the plant needs to have a name so you can find it later '
                                   'when you\'re adding your own plants!',
                       validators=[
                           validators.DataRequired('Must supply a name')
                       ])
    max_temperature = IntegerField(label='Max temperature',
                                   description='Specify the plants threshold for its maximum temperature',
                                   validators=[
                                       validators.Optional()
                                   ])
    min_temperature = IntegerField(label='Min temperature',
                                   description='Specify the plants threshold for its minimum temperature',
                                   validators=[
                                       validators.Optional()
                                   ])
    moisture = SelectField(label='Pin type *',
                           description='Specify what kind of soil you the plant need',
                           choices=[('dry', 'Dry soil'), ('humid', 'Humid soil'), ('water', 'Water')],
                           validators=[
                               validators.DataRequired('You must specify what kind of soil the plant need')
                           ])
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
