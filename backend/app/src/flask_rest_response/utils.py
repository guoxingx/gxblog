
from flask import jsonify as flask_jsonify

from .configs import DefaultConfigs


_configs = DefaultConfigs


def _config_key_name(name):
    return name
    # return 'FLASK_REST_RESPONSE_{}'.format(name.upper())


def init_config(**kw):
    _configs.update(kw)


def config_value(key):
    return _configs.get(_config_key_name(key))


def formatted(code, data, errmsg, jsonify=None):
    if jsonify is None:
        jsonify = config_value('jsonify')

    code_name = config_value('key_name_code')
    errmsg_name = config_value('key_name_errmsg')
    data_name = config_value('key_name_data')

    try:
        code = int(code)
    except ValueError:
        raise ValueError('unable to integerized code {}'.format(code))

    formatted_data = {
        code_name: int(code),
        data_name: data or '',
        errmsg_name: errmsg
    }
    if jsonify:
        return flask_jsonify(formatted_data)
    return formatted_data
