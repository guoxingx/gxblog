
import logging

from flask import Blueprint, jsonify, current_app
main = Blueprint('main', __name__)


@main.errorhandler(Exception)
def internal_server_error(e):
    raise e


from . import views
