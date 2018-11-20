# views.py
import json

from flask import jsonify, make_response
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

        sender = args["sender"]
        recipient = args["recipient"]
        pickup = args["pickup"]
        destination = args["destination"]
        weight = args["weight"]

        parcel = ParcelOrderModel(sender, recipient, pickup, destination,
                                  weight)
        parcel_order = self.order_manager.save(parcel)
        parcel_order = {
            "sender": parcel_order.sender,
            "recipient": parcel_order.recipient,
            "pickup": parcel_order.pickup,
            "destination": parcel_order.destination,
            "weight": parcel_order.weight
        }
        payload = {"message": "Success",
                   "parcel_order": parcel_order}
        return make_response(jsonify(payload), 201)

    def get(self):
        parcel_objects = self.order_manager.fetch_all()
        orders = []
        for parcel in parcel_objects:
             order = {
                "sender": parcel.sender,
                "recipient": parcel.recipient,
                "pickup": parcel.pickup,
                "destination": parcel.destination,
                "weight": floate(parcel.weght)
             }
             orders.append(order)

        payload = {
            "message": "Success",
            "parcel_orders": orders
        }
        return make_response(jsonify(payload), 200)
