import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    return app
