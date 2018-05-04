
from flask import Blueprint, jsonify
main = Blueprint('main', __name__)


@main.app_errorhandler(Exception)
def internal_server_error(e):
    raise e


from . import views
