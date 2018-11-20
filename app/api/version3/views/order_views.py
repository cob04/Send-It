# views.py
from flask_restful import reqparse, Resource

from ..models.orders import ParcelOrderModel, ParcelOrderManager


class ParcelOrderList(Resource):

    def __init__(self):
        self.order_manager = ParcelOrderManager()

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

        parcel = ParcelOrderModel(**args)
        parcel_order = self.order_manager.save(parcel)
        payload = {
            "message": "Success",
            "parcel_order": parcel.to_dict()
        }
        return payload, 201

    def get(self):
        parcel_objects = self.order_manager.fetch_all()
        orders = [parcel.to_dict() for parcel in parcel_objects]
        payload = {
            "message": "Success",
            "parcel_orders": orders
        }
        return payload, 200


class ParcelOrder(Resource):

    def __init__(self):
        self.order_manager = ParcelOrderManager()

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
