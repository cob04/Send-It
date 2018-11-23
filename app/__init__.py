# __init__.py

from flask import Flask
from flask_jwt_extended import JWTManager
from config import config
from .api.version1 import v1
from .api.version2 import v2
from .api.version3 import v3

from .db_config import create_tables


def create_app(config_name='testing'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config["JWT_SECRET_KEY"] = "thisisabigsecret"
    jwt = JWTManager(app)
    create_tables()
    app.register_blueprint(v1)
    app.register_blueprint(v2)
    app.register_blueprint(v3)
    return app
