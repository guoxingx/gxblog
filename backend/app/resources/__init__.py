
from flask import Blueprint, jsonify, current_app
from flask_restful import Api


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


@api_blueprint.errorhandler(Exception)
def internal_server_error(e):
    current_app.logger.exception(e)
    return jsonify({'code': 500, 'message': 'internal server error'})


def register_api(resource, route, endpoint=None):
    api_route = "/{}".format(route)
    api_endpoint = "{}".format(endpoint or route.replace('/', '_'))
    api.add_resource(resource, api_route, endpoint=api_endpoint)


from .blog import Blogs, Blog
register_api(Blogs, 'blogs')
register_api(Blog, 'blogs/<id>')


from .ethereum import (
    EthStatus,
    Accounts,
    Balance,
    TestEtherCoin,
    BetOnEtherList,
    BetOnEtherBetList,
    BetOnEtherWithdraw
)
register_api(EthStatus, 'eth/status')
register_api(Accounts, 'eth/accounts')
register_api(TestEtherCoin, 'eth/testether')
register_api(Balance, 'eth/accounts/<address>/balance')
register_api(BetOnEtherList, 'eth/betonethers')
register_api(BetOnEtherBetList, 'eth/betonethers/<id>/bets')
register_api(BetOnEtherWithdraw, 'eth/betonethers/<id>/withdraw')
