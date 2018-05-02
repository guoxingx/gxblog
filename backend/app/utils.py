
import os

from werkzeug.datastructures import MultiDict
from flask import request
# from web3.auto import w3
from web3 import Web3, HTTPProvider
from eth_utils import to_checksum_address

from .db import db


CONFIG = {}


def get_w3():
    return Web3(HTTPProvider(config_value('ETH_RPC_URL')))


def populate_config(config):
    global CONFIG
    for key in dir(config):
        if key.isupper():
            CONFIG[key] = getattr(config, key)


def config_value(key):
    global CONFIG
    return CONFIG.get(key)


def get_static_dir(target=None):
    abs_dir = os.path.dirname(__file__)
    res = '{}/static'.format(abs_dir)
    if target:
        res = '{}/{}'.format(res, target)
    return res


def get_images_dir():
    return get_static_dir('images')


def remove_static_file(filename):
    path = '{}/{}'.format(get_static_dir(), filename)
    try:
        os.system('rm {}'.format(path))
    except FileNotFoundError as e:
        print(e)


def remove_images_file(filename):
    path = '{}/{}'.format(get_images_dir(), filename)
    try:
        os.system('rm {}'.format(path))
    except FileNotFoundError as e:
        print(e)


def db_commit():
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise


def get_form(form_class, _dict):
    data = {}
    for k, v in _dict.items():
        if v is not None:
            data[k] = v
    return form_class(MultiDict(data))


def form_by_json_request(form_class):
    return get_form(form_class, request.json or request.form)


def to_checked_address(address):
    """
    非混合大小写的addres会报错，不知道是否是bug
    将address转换成混合大小写
    """
    res = to_checksum_address(address)
    if res.lower() == address or res.upper() == address:
        return res
    return address


def auto_mine():
    """
    """
    w3 = get_w3()
    eth = w3.eth
    miner = w3.miner
    if len(eth.getBlock('pending').transactions) > 0:
        if not eth.mining:
            print('start mine')
            miner.start(1)
    else:
        if eth.mining:
            print('stop mine')
            miner.stop()
