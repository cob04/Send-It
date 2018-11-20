from flask import Blueprint
from flask_restful import Api

v3 = Blueprint('v3', __name__, url_prefix='/api/v3')
api = Api(v3)
