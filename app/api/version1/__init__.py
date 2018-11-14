# __init__.py

from flask import Blueprint
from flask_restful import Api

from .views import ParcelOrderList


v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
api = Api(v1)

api.add_resource(ParcelOrderList, '/parcels/', strict_slashes=False)
