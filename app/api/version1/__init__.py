from flask import Blueprint
from flask_restful  import Api, Resource

from .views import ParcelOrder, ParcelOrderList


v1 = Blueprint('v1', __name__, url_prefix='/api/v1')
api = Api(v1)


api.add_resource(views.ParcelOrderList, '/parcels/',
                 strict_slashes=False)
api.add_resource(views.ParcelOrder, '/parcels/<int:order_id>',
                 strict_slashes=False)
