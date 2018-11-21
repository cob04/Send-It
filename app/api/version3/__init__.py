from flask import Blueprint
from flask_restful import Api

from .views import order_views as orders
from .views import user_views as users


v3 = Blueprint('v3', __name__, url_prefix='/api/v3')
api = Api(v3)

api.add_resource(orders.ParcelOrderList, '/parcels/', strict_slashes=False)
api.add_resource(orders.ParcelOrder, '/parcels/<parcel_id>',
                 strict_slashes=False)

api.add_resource(orders.UserParcelOrderCancel,
                 '/parcels/<int:parcel_id>/cancel',
                 strict_slashes=False)

api.add_resource(users.UserList, '/auth/signup', strict_slashes=False)
