# views.py

from flask import jsonify, make_response, request
from flask_restful import Resource

from .models import CANCELLED
from .models import ParcelOrderStore


class ParcelOrderList(Resource, ParcelOrderStore):

    def __init__(self):
        self.store = ParcelOrderStore()

    def post(self):
        request_data = request.get_json()
        user_id = request_data["user_id"]
        sender = request_data["sender"]
        recipient = request_data["recipient"]
        pickup = request_data["pickup"]
        destination = request_data["destination"]
        weight = request_data["weight"]

        parcel_order = self.store.save(user_id, sender, recipient, pickup,
                                       destination, weight)
        payload = {"message": "Success",
                   "parcel_order": parcel_order}
        return make_response(jsonify(payload), 201)

    def get(self):
        orders = self.store.all()
        payload = {
            "message": "Success",
            "parcel_orders": orders
        }
        return make_response(jsonify(payload), 200)


class ParcelOrder(Resource, ParcelOrderStore):

    def __init__(self):
        self.store = ParcelOrderStore()

    def get(self, order_id):
        try:
            order = self.store.fetch_by_id(order_id)
            payload = {
                "message": "Success",
                "parcel_order": order
            }
            return make_response(jsonify(payload), 200)
        except IndexError:
            payload = {
                "message": "Sorry, we cannot find such an order",
                "error": "Not found"
            }
            return make_response(jsonify(payload), 404)


class ParcelOrderCancellation(Resource, ParcelOrderStore):

    def __init__(self):
        self.store = ParcelOrderStore()

    def put(self, order_id):
        request_data = request.get_json()
        status = request_data["status"]
        try:
            if status == CANCELLED:
                order = self.store.cancel_by_id(order_id)
                payload = {
                    "message": "Success",
                    "parcel_order": order
                }
                return make_response(jsonify(payload), 201)
            else:
                payload = {
                    "message": "Please set status field to %s" % CANCELLED,
                    "error": "Invalid field entry"
                }
                return make_response(jsonify(payload), 400)
        except IndexError:
            payload = {
                "message": "Sorry, we cannot find that order",
                "error": "Not found"
            }
            return make_response(jsonify(payload), 404)


class UserParcelOrderList(Resource, ParcelOrderStore):

    def __init__(self):
        self.store = ParcelOrderStore()

    def get(self, user_id):
        order = self.store.fetch_by_user_id(user_id)
        payload = {
            "message": "Success",
            "parcel_orders": order
        }
        return make_response(jsonify(payload))
