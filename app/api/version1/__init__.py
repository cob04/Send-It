# __init__.py

from flask import Blueprint
from flask_restful import Api

from .views import (ParcelOrder, ParcelOrderList, UserParcelOrderList,
                    ParcelOrderCancellation)


v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
api = Api(v1)

api.add_resource(ParcelOrderList, '/parcels/', strict_slashes=False)
api.add_resource(ParcelOrder, '/parcels/<int:order_id>',strict_slashes=False)
api.add_resource(ParcelOrderCancellation, '/parcels/<int:order_id>/cancel',
                 strict_slashes=False)
api.add_resource(UserParcelOrderList, '/users/<int:user_id>/parcels',
                 strict_slashes=False)
