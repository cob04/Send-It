from flask import Blueprint
from flask_restful import Api

from .views import order_views as views


v3 = Blueprint('v3', __name__, url_prefix='/api/v3')
api = Api(v3)

api.add_resource(views.ParcelOrderList, '/parcels/', strict_slashes=False)
api.add_resource(views.ParcelOrder, '/parcels/<parcel_id>', strict_slashes=False)

api.add_resource(views.UserParcelOrderCancel, '/parcels/<int:parcel_id>/cancel',
                 strict_slashes=False)
