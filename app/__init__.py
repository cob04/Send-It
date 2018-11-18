# __init__.py

from flask import Flask
from .api.version1 import v1
from .api.version2 import v2


def create_app():
    app = Flask(__name__)
    app.register_blueprint(v1)
    app.register_blueprint(v2)
    return app
