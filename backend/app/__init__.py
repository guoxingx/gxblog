#!coding:utf-8

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler

from .db import db
from .resources import api
from config import config


login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    api.init_app(app)
    login_manager.init_app(app)

    CORS(app, max_age=86400)

    from .main import main as main_blueprint
    main_blueprint.url_prefix = '/admin'
    app.register_blueprint(main_blueprint)

    # from .admin import manager as manager_blueprint
    # manager_blueprint.url_prefix = '/admin'
    # app.register_blueprint(manager_blueprint)

    # from .admin import init_admin
    # init_admin(app, db)

    from .src.eth import Connector
    coon = Connector()

    def sensor():
        coon.auto_mine_in_test()

    sched = BackgroundScheduler(daemon=True)
    sched.add_job(sensor, 'interval', seconds=5)
    sched.start()

    return app
