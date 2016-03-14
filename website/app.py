#!/usr/bin/env python
# coding=utf-8
from flask import Flask
from flask_wtf.csrf import CsrfProtect

from website.AWSError import AWSError
from website.app_settings import ProductionConfig
from website.backend import root, own_plant, plant, pump

app = Flask(__name__, template_folder='./public', static_url_path='/static', static_folder='./public')


def create_app(config_object=ProductionConfig):
    """
    :param config_object:
    :return: Flask
    """
    # app = Flask(__name__, template_folder='./public', static_url_path='/static', static_folder='./public')
    app.config.from_object(config_object)

    register_blueprints(app)
    setup_csrf(app)

    return app


def register_blueprints(app):
    """
    :type app: Flask
    :param app:

    :return: None
    """

    app.register_blueprint(root.blueprint)
    app.register_blueprint(own_plant.blueprint)
    app.register_blueprint(plant.blueprint)
    app.register_blueprint(pump.blueprint)

    return None


def setup_csrf(app):
    # Initiate Flask-WTForms CSRF protection
    csrf = CsrfProtect()
    csrf.init_app(app)
    return None


@app.errorhandler(AWSError)
def handle_aws_error(error):
    return error.get_template()
