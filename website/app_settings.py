#!/usr/bin/env python
# coding=utf-8


class Config(object):
    pass


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'production'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SECRET_KEY = ENV


class TestingConfig(Config):
    def __init__(self, db):
        self.DB_NAME = db

    DB_NAME = None
    ENV = 'testing'
    TESTING = True
    SECRET_KEY = ENV
    WTF_CSRF_ENABLED = False
