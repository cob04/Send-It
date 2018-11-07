# app/__init__.py

from flask import Flask


def create_app():
    app = Flask(__name__)
    # app.config.from_object()

    from .api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1',
                           strict_slashes=False)
    return app
