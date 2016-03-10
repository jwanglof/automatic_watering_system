#!/usr/bin/env python
# coding=utf-8
from flask import Flask

from website.backend import root
from website.backend import own_plant


def create_app():
    """
    :return: Flask
    """
    app = Flask(__name__, static_folder='./frontend/static', static_url_path='/static')

    register_blueprints(app)

    return app


def register_blueprints(app):
    """
    :type app: Flask
    :param app:

    :return: None
    """

    app.register_blueprint(root.blueprint)
    app.register_blueprint(own_plant.blueprint)

    return None
