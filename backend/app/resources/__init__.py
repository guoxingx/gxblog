
from flask_restful import Api


api = Api()


def register_api(resource, route, endpoint=None):
    api_route = "/api/{}".format(route)
    api_endpoint = "api_{}".format(endpoint or route.replace('/', '_'))
    api.add_resource(resource, api_route, endpoint=api_endpoint)


from .articles import Articles, Article
register_api(Articles, 'articles')
register_api(Article, 'articles/<int:_id>')

from .betonether import BetOnEtherList
register_api(BetOnEtherList, 'betonethers')
