from flask import Blueprint
from flask_restful import Api

from .views.order_views import ParcelOrder, ParcelOrderList


v3 = Blueprint('v3', __name__, url_prefix='/api/v3')
api = Api(v3)

api.add_resource(ParcelOrderList, '/parcels/', strict_slashes=False)
api.add_resource(ParcelOrder, '/parcels/<parcel_id>', strict_slashes=False)
