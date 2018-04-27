#!coding:utf-8

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_login import LoginManager

from .db import db
from config import config


api = Api()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    CORS(app, max_age=86400)

    from .main import main as main_blueprint
    main_blueprint.url_prefix = '/admin'
    app.register_blueprint(main_blueprint)

    def register_api(resource, route, endpoint=None):
        api_route = "/api/{}".format(route)
        api_endpoint = "api_{}".format(endpoint or route.replace('/', '_'))
        api.add_resource(resource, api_route, endpoint=api_endpoint)

    from .resources.articles import Articles, Article
    register_api(Articles, 'articles')
    register_api(Article, 'articles/<int:_id>')

    api.init_app(app)

    # from .admin import manager as manager_blueprint
    # manager_blueprint.url_prefix = '/admin'
    # app.register_blueprint(manager_blueprint)

    # from .admin import init_admin
    # init_admin(app, db)

    return app
