#!/usr/bin/env python
# coding=utf-8

from wtforms import Form, validators, StringField
import wtforms_json
wtforms_json.init()


class OwnPlantValidation(Form):
    plant_id = StringField('plant_id', [validators.DataRequired('You must apply which plant this entry is for!')])
    description = StringField('description', [validators.Optional()])
