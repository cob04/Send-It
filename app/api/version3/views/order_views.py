# views.py
from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..exceptions import ParcelNotFoundError, ApplicationError
from ..models.orders import ParcelOrderModel, ParcelOrderManager
from ..models.users import ADMIN, NORMAL, UserManager


class ParcelOrderList(Resource):
    """Resource for adding a new parcel and retrieving all parcels.
    """
    def __init__(self):
        self.order_manager = ParcelOrderManager()

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
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
        user_id = get_jwt_identity()
        parcel = ParcelOrderModel(user_id, **args)
        self.order_manager.save(parcel)
        payload = {
            "message": "Success",
            "parcel_order": parcel.to_dict()
        }
        return payload, 201

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        manager = UserManager()
        user = manager.fetch_by_id(user_id)
        if user.role == ADMIN:
            parcel_objects = self.order_manager.fetch_all()
        else:
            parcel_objects = self.order_manager.fetch_all_user_parcels(user_id)
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
        try:
            parcel = self.order_manager.fetch_by_id(parcel_id)
            payload = {
                "message": "Success",
                "parcel_order": parcel.to_dict()
            }
            return payload, 200
        except ParcelNotFoundError:
            payload = {
                "message": "Sorry, we cannot find such a parcel",
                "error": "Parcel not found"
            }
        except ApplicationError:
            payload = {
                "message": "Sorry, sonething went wrong",
                "error": "Application error"
            }

class UserParcelOrderCancel(Resource):
    """Resource to cancel a parcel."""
    def __init__(self):
        self.order_manager = ParcelOrderManager()

    @jwt_required
    def put(self, parcel_id):
        try:
            parcel = self.order_manager.cancel_by_id(parcel_id)
            payload = {
                "message": "Success",
                "parcel_order": parcel.to_dict()
            }
            return payload, 201
        except ParcelNotFoundError:
            payload = {
                "message": "Sorry,  we cannnot find such a parcel",
                "error": "Parcel not found"
            }

        except ApplicationError:
            payload = {
                "message": "Sorry, something went wrong",
                "error": "Application error"
            }
            return payload, 500


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
        try:
            user_id = get_jwt_identity()
            parcel = self.order_manager.update_destination(parcel_id, destination)
            # check if the user owns the parcel.
            if user_id != parcel.user_id:
                payload = {
                    "message": "Sorry, you are unauthorized",
                }
                return payload, 401
            else:
                payload = {
                    "message": "Success",
                    "parcel_order": parcel.to_dict()
                }
                return payload, 201

        except ParcelNotFoundError:
            payload = {
                "message": "Sorry, we cannot find such a parcel",
                "error": "Parcel not found",
            }
            return payload, 404

        except ApplicationError:
            payload = {
                "message": "Sorry, something went wrong",
                "error": "Application error"
            }
            return payload, 500


class ParcelUpdateStatus(Resource):
    """Resource to change a pardel status."""
    def __init__(self):
        self.manager = ParcelOrderManager()

    @jwt_required
    def put(self, parcel_id):
        user_id = get_jwt_identity()
        manager = UserManager()
        user = manager.fetch_by_id(user_id)
        if user.role != ADMIN:
            payload = {
                "message": "Sorry, you are unauthorized",
            }
            return payload, 401
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=True,
                            help="A status is required")
        args = parser.parse_args()
        status = args["status"]
        try:
            parcel = self.manager.update_status(parcel_id, status)
            payload = {
                "message": "Success",
                "parcel_order": parcel.to_dict()
            }
            return payload, 201

        except ParcelNotFoundError:
            payload = {
                "message": "Sorry, we cannot find such a parcel",
                "error": "Parcel not found",
            }
            return payload, 404

        except ApplicationError:
            payload = {
                "message": "Sorry, something went wrong",
                "error": "Application error"
            }
            return payload, 500


class ParcelUpdatePresentLocation(Resource):
    """Resource to change a pardel present location."""
    def __init__(self):
        self.manager = ParcelOrderManager()

    @jwt_required
    def put(self, parcel_id):
        user_id = get_jwt_identity()
        manager = UserManager()
        user = manager.fetch_by_id(user_id)
        if user.role != ADMIN:
            payload = {
                "message": "Sorry, you are unauthorized",
            }
            return payload, 401

        parser = reqparse.RequestParser()
        parser.add_argument('present_location', type=str, required=True,
                            help="A location is required")
        args = parser.parse_args()
        present_location = args["present_location"]
        try:
            parcel = self.manager.update_present_location(parcel_id, present_location)
            payload = {
                "message": "Success",
                "parcel_order": parcel.to_dict()
            }
            return payload, 201

        except ParcelNotFoundError:
            payload = {
                "message": "Sorry, we cannot find such a parcel",
                "error": "Parcel not found",
            }
            return payload, 404

        except ApplicationError:
            payload = {
                "message": "Sorry, something went wrong",
                "error": "Application error"
            }
            return payload, 500
