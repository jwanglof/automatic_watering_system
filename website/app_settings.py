#!/usr/bin/env python
# coding=utf-8


class Config(object):
    pass


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True


class TestingConfig(Config):
    def __init__(self, db):
        self.DB_NAME = db

    DB_NAME = None
    ENV = 'testing'
    TESTING = True
