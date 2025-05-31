import os

class Config:
    TESTING = False
    SECRET_KEY='dev'
    SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite"
    JWT_SECRET_KEY = "super-secret"

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    SECRET_KEY='dev'
    SQLALCHEMY_DATABASE_URI="sqlite:///db.sqlite"
    JWT_SECRET_KEY = "super-secret"

class TestingConfig(Config):
    TESTING = True
    SECRET_KEY='test'
    SQLALCHEMY_DATABASE_URI="sqlite://"
    JWT_SECRET_KEY = "test"