#!coding:utf-8

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    api = Api(app)

    def register_api(resource, route, endpoint=None):
        api_route = "/api/{}".format(route)
        api_endpoint = "api_{}".format(endpoint or route.replace('/', '_'))
        api.add_resource(resource, api_route, endpoint=api_endpoint)

    CORS(app, max_age=86400)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .resources.images import Images
    register_api(Images, 'images/<image_type>')

    from .resources.articles import Articles, Article
    register_api(Articles, 'articles')
    register_api(Article, 'articles/<int:_id>')

    from .resources.informations import Informations
    register_api(Informations, 'informations/<_id>')

    return app
