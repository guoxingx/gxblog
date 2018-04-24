
import os

from werkzeug.datastructures import MultiDict
from flask import request

from .db import db


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
