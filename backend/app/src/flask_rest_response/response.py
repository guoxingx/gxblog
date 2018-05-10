#!coding: utf-8

import functools

from flask import request, abort

from .errors import Error
from .utils import formatted


def json_required():
    """
    response 400 if request not in json format.
    """
    def wrapper(func):
        @functools.wraps(func)
        def decorator(*args, **kw):
            if request.method not in ['GET', 'DELETE']:
                if not request.json:
                    if 'application/json' not in request.headers.get('content-type'):
                        abort(400)
            response = func(*args, **kw)
            return response
        return decorator
    return wrapper


def response():
    """
    response success:
        return data.

    response fail with errorinfo:
        return 10030, errorinfo.

    response fail with errorinfo and data:
        return 10030, data, errorinfo
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            res = func(*args, **kw)

            # return data
            if not isinstance(res, tuple):
                return formatted(0, res, '')

            # return 20002, error
            if len(res) == 2:
                if isinstance(res[0], int):
                    if res[0] == 0:
                        # success
                        return formatted(res[0], res[1], '')
                    # error
                    return formatted(res[0], '', res[1])
                raise AttributeError

            # return 20002, data, error
            if len(res) == 3:
                if isinstance(res[0], int):
                    return formatted(res[0], res[1], res[2])
                raise AttributeError

        return wrapper
    return decorator
