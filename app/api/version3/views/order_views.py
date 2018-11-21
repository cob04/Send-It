# views.py
from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required 

from ..models.orders import ParcelOrderModel, ParcelOrderManager


class ParcelOrderList(Resource):
    """Resource for adding a new parcel and retrieving all parcels.
    """
    def __init__(self):
        self.order_manager = ParcelOrderManager()

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True,
                            help="Order must have a user_id field")
        parser.add_argument('sender', type=str, required=True,
                            help="Order must have a sender")
        parser.add_argument('recipient', type=str, required=True,
                            help="Order must have a recipient")
        parser.add_argument('pickup', type=str, required=True,
                            help="Order must have a pickup")
        parser.add_argument('destination', type=str, required=True,
                            help="Order must have a destination")
        parser.add_argument('weight', type=str, required=True,
                            help="Order must have a weight")

        args = parser.parse_args()

        parcel = ParcelOrderModel(**args)
        self.order_manager.save(parcel)
        payload = {
            "message": "Success",
            "parcel_order": parcel.to_dict()
        }
        return payload, 201

    @jwt_required
    def get(self):
        parcel_objects = self.order_manager.fetch_all()
        orders = [parcel.to_dict() for parcel in parcel_objects]
        payload = {
            "message": "Success",
            "parcel_orders": orders
        }
        return payload, 200


class ParcelOrder(Resource):
    """Resource for a getting a single parcel."""
    def __init__(self):
        self.order_manager = ParcelOrderManager()

    @jwt_required
    def get(self, parcel_id):
        parcel = self.order_manager.fetch_by_id(parcel_id)
        if parcel:
            payload = {
                "message": "Success",
                "parcel_order": parcel.to_dict()
            }
            return payload, 200
        else:
            payload = {
                "message": "Sorry, we cannot find such a parcel",
                "error": "Not found"
            }

class UserParcelOrderCancel(Resource):
    """Resource to cancel a parcel."""
    def __init__(self):
        self.order_manager = ParcelOrderManager()

    @jwt_required
    def put(self, parcel_id):
        parcel = self.order_manager.cancel_by_id(parcel_id)
        payload = {
            "message": "Success",
            "parcel_order": parcel.to_dict()
        }
        return payload, 201


class ParcelUpdateDestination(Resource):
    """Resource to change a parcel's destination."""
    def __init__(self):
        self.order_manager = ParcelOrderManager()

    @jwt_required
    def put(self, parcel_id):
        parser = reqparse.RequestParser()
        parser.add_argument('destination', type=str, required=True,
                            help="Parcel must have a destination")
        args = parser.parse_args()
        destination = args["destination"]
        parcel = self.order_manager.update_destination(parcel_id, destination)
        payload = {
            "message": "Success",
            "parcel_order": parcel.to_dict()
        }
        return payload, 201


class ParcelUpdateStatus(Resource):
    """Resource to change a pardel status."""
    def __init__(self):
        self.manager = ParcelOrderManager()

    @jwt_required
    def put(self, parcel_id):
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=True,
                            help="A status is required")
        args = parser.parse_args()
        status = args["status"]
        parcel = self.manager.update_status(parcel_id, status)
        payload = {
            "message": "Success",
            "parcel_order": parcel.to_dict()
        }
        return payload, 201
