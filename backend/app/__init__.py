#!coding:utf-8

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
# from flask_socketio import SocketIO, emit

from .db import db
from .utils import populate_config
# from .resources import api
from config import config


login_manager = LoginManager()
# socketio = SocketIO()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    populate_config(config[config_name])

    db.init_app(app)
    # socketio.init_app(app)
    login_manager.init_app(app)

    CORS(app, max_age=86400)

    from .resources import api_blueprint
    api_blueprint.url_prefix = '/api'
    app.register_blueprint(api_blueprint)

    from .main import main as main_blueprint
    main_blueprint.url_prefix = '/admin'
    app.register_blueprint(main_blueprint)

    from apscheduler.schedulers.background import BackgroundScheduler
    from .utils import auto_mine
    if app.config.get('ETH_MODE') == 'test':
        def sensor():
            auto_mine()

        sched = BackgroundScheduler(daemon=True)
        sched.add_job(sensor, 'interval', seconds=5)
        sched.start()

    return app
