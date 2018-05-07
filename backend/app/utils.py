
import os

from werkzeug.datastructures import MultiDict
from flask import request, current_app
# from web3.auto import w3
from web3 import Web3, HTTPProvider
from eth_utils import to_checksum_address
from requests.exceptions import ReadTimeout

from .db import db


CONFIG = {}


def get_w3():
    return Web3(HTTPProvider(config_value('ETH_RPC_URL'), request_kwargs={'timeout': 5}))


def get_node_status(show_balance=False):
    if current_app.config.get('ETH_MODE') == 'test':
        return {
            'status': 0,
            'peer_count': 0,
            'message': 'private chain'
        }
    balance = None
    status = 0
    message = 'working'
    w3 = get_w3()
    try:
        peer_count = w3.net.peerCount
    except ReadTimeout as e:
        peer_count = 0
    try:
        balance = w3.eth.getBalance(w3.eth.accounts[0])
    except ValueError as e:
        if e.args[0].get('code') == -32000:
            if peer_count > 0:
                status = 1
                message = 'syncing'
            else:
                status = 2
                message = 'warting for peers'
        else:
            raise e

    res = {
        'status': status,
        'peer_count': peer_count,
        'message': message
    }
    if show_balance:
        res['balance'] = balance
    return res


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


def get_saved_blog_files():
    return os.listdir(get_blog_files_dir())


def get_saved_images():
    return os.listdir(get_images_dir())


def save_image(image, filename):
    if '.' not in filename:
        filename = '{}.png'.format(filename)
    save_path = '{}/{}'.format(get_images_dir(), filename)
    image.save(save_path)


def get_blog_files_dir():
    return get_static_dir('blogs')


def save_blog_file(blogfile, filename):
    save_path = '{}/{}.html'.format(get_blog_files_dir(), filename)
    blogfile.save(save_path)
