#!/usr/bin/env python
# coding=utf-8
from flask import Flask

from website.app_settings import ProductionConfig
from website.backend import root
from website.backend import own_plant


def create_app(config_object=ProductionConfig):
    """
    :param config_object:
    :return: Flask
    """
    app = Flask(__name__, static_folder='./frontend/static', static_url_path='/static')
    app.config.from_object(config_object)

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
