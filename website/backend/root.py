#!/usr/bin/env python
# coding=utf-8
from flask import Blueprint, render_template

blueprint = Blueprint('root', __name__, url_prefix='/')


@blueprint.route('/')
def root():
    # form = OwnPlantForm.OwnPlantForm()
    return render_template('root.html')
