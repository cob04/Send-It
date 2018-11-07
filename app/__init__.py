# app/__init__.py

from  flask import Flask
from .api.version1 import v1


def create_app():
    app = Flask(__name__)
    app.register_blueprint(v1)

    return app
