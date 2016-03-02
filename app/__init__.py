from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from config import config, Config
# from celery import Celery


bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# celery = Celery('__name__', broker=Config.CELERY_BROKER_URL)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    # celery.conf.update(app.config)

    from .players import players as players_blueprint
    app.register_blueprint(players_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

