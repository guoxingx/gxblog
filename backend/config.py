# coding: utf-8

import os
import re


mysql_user = os.environ.get('MYSQL_USER')
mysql_pass = os.environ.get('MYSQL_PASSWORD')
mysql_db = os.environ.get('MYSQL_DATABASE')


def fix_eth_rpc_url(eth_rpc_url):
    _, url = eth_rpc_url.split('://')
    url, port = url.split(':')
    if '.' in url:
        return eth_rpc_url
    os.system('ping -c 1 {} >/tmp/abc  2>&1'.format(url))
    with open('/tmp/abc') as f:
        content = f.read()
        try:
            url = re.findall('\(.*\)', content)[0][1:-1]
            return 'http://{}:{}'.format(url, port)
        except IndexError:
            return eth_rpc_url


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ittaidaregaiyashitekurerudarou'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@0.0.0.0:3306/{}?charset=utf8mb4'.format(mysql_user, mysql_pass, mysql_db)
    REDIS_URL = 'redis://@0.0.0.0:6379/0'

    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    ETH_RPC_URL = 'http://localhost:8545'
    ETH_COINBASE_PASSWORD = os.environ.get('ETH_COINBASE_PASSWORD')


class TestConfig(Config):
    DEBUG = True
    FLASK_DEBUG = 1

    REDIS_URL = 'redis://@0.0.0.0:6379/0'
    ETH_RPC_URL = 'http://localhost:8545'


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = 1

    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@mysql/{}?charset=utf8mb4'.format(mysql_user, mysql_pass, mysql_db)
    REDIS_URL = 'redis://@redis/0'
    ETH_RPC_URL = fix_eth_rpc_url('http://ethnode:8545')


config = {
    'test': TestConfig,
    'dev': DevelopmentConfig,
}
