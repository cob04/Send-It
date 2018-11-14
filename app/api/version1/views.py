# views.py

from flask import jsonify, make_response, request
from flask_restful import Resource

from .models import ParcelOrderStore


class ParcelOrderList(Resource, ParcelOrderStore):

    def __init__(self):
        self.store = ParcelOrderStore()

    def post(self):
        request_data = request.get_json()
        sender = request_data["sender"]
        recipient = request_data["recipient"]
        pickup = request_data["pickup"]
        destination = request_data["destination"]
        weight = request_data["weight"]

        parcel_order = self.store.save(sender, recipient, pickup, destination,
                                       weight)
        payload = {"message": "success",
                   "parcel_order": parcel_order}
        return make_response(jsonify(payload), 201)

    def get(self):
        orders = self.store.all()
        payload = {
            "message": "success",
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
                "message": "success",
                "parcel_order": order
            }
            return make_response(jsonify(payload), 200)
        except IndexError:
            payload = {
                "message": "failed",
                "error": "Not found"
            }
            return make_response(jsonify(payload), 404)

    def put(self, order_id):
        request_data = request.get_json()
        sender = request_data["sender"]
        recipient = request_data["recipient"]
        pickup = request_data["pickup"]
        destination = request_data["destination"]
        weight = request_data["weight"]
        status = request_data["status"]

        parcel_order = self.store.update_by_id(order_id, sender, recipient, pickup,
                                       destination, weight, status)
        payload = {"message": "success",
                   "parcel_order": parcel_order}
        return make_response(jsonify(payload), 201)
