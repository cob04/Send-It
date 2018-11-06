# app/api/__init__.py

from flask import Blueprint
from flask_restful import Api

from .version1 import views


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


api.add_resource(views.ParcelOrderList, '/parcels/',
                 strict_slashes=False)
api.add_resource(views.ParcelOrder, '/parcels/<int:order_id>',
                 strict_slashes=False)
