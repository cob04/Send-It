# __init__.py

from flask import Blueprint
from flask_restful import Api

from .views import (ParcelOrder, ParcelOrderList, UserParcelOrderList,
                    ParcelOrderCancellation, UserList, AuthLogin)


v2 = Blueprint('v2', __name__, url_prefix='/api/v2')
api = Api(v2)

api.add_resource(ParcelOrderList, '/parcels/', strict_slashes=False)
api.add_resource(ParcelOrder, '/parcels/<int:order_id>', strict_slashes=False)
api.add_resource(ParcelOrderCancellation, '/parcels/<int:order_id>/cancel',
                 strict_slashes=False)

api.add_resource(UserList, '/users',
                 strict_slashes=False)
api.add_resource(UserParcelOrderList, '/users/<int:user_id>/parcels',
                 strict_slashes=False)

api.add_resource(AuthLogin, '/auth/login', strict_slashes=False)
