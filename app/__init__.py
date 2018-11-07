# app/__init__.py

from  flask import Flask
from .api.version1 import v1


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    app.register_blueprint(v1)

    return app
