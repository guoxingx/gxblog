# coding: utf-8

import os


mysql_user = os.environ.get('MYSQL_USER')
mysql_pass = os.environ.get('MYSQL_PASSWORD')
mysql_db = os.environ.get('MYSQL_DATABASE')


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ittaidaregaiyashitekurerudarou'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@0.0.0.0:3306/{}?charset=utf8mb4'.format(mysql_user, mysql_pass, mysql_db)
    REDIS_URL = 'redis://@0.0.0.0:6379/0'

    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')


class TestConfig(Config):
    DEBUG = True
    FLASK_DEBUG = 1

    REDIS_URL = 'redis://@0.0.0.0:6379/0'


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = 1

    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@mysql/{}?charset=utf8mb4'.format(mysql_user, mysql_pass, mysql_db)
    REDIS_URL = 'redis://@redis_conn/0'


config = {
    'test': TestConfig,
    'dev': DevelopmentConfig,
}
