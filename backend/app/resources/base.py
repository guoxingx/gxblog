
import functools

from flask import abort, request
from flask.views import MethodViewType
from flask_restful import Resource
from flask_login import current_user


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        if not current_user.is_authenticated:
            abort(401)
        return func(*args, **kw)
    return wrapper


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


class BaseResourceMeta(MethodViewType):

    def __new__(cls, name, bases, dct):
        """
        Add decorators to Resource.

        decorator ahead in the list will be execute first.
        """
        c_decorators = dct.get('decorators', [])
        decorators = [json_required()]
        decorators.extend(c_decorators)
        dct['decorators'] = decorators
        return super(BaseResourceMeta, cls).__new__(cls, name, bases, dct)


class BaseResource(Resource, metaclass=BaseResourceMeta):
    pass
