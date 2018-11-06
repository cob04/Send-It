# views.py

from flask import jsonify, make_response, request, jsonify
from flask_restful import Resource

from .models import ParcelOrderStore

from .exceptions import OrderNotFoundError


class ParcelOrderList(Resource):

    def __init__(self):
        self.store = ParcelOrderStore()

    def get(self):
        parcel_orders = self.store.all()
        payload = {
            "message": "success",
            "parcel_orders": parcel_orders
        }
        return make_response(jsonify(payload), 200)

    def post(self):
        request_data = request.get_json()
        sender = request_data['sender']
        recipient = request_data['recipient']
        pickup = request_data['pickup']
        destination = request_data['destination']
        weight = request_data['weight']

        payload = self.store.save(sender, recipient, pickup,
                                  destination, weight)

        return make_response(jsonify(payload), 201)


class ParcelOrder(Resource):

    def __init__(self):
        self.store = ParcelOrderStore()

    def get(self, order_id):
        try:
            parcel_order = self.store.fetch_by_id(order_id)
            payload = {"message": "success",
                       "parcel_order": parcel_order
                  }
            return make_response(jsonify(payload), 200)
        except OrderNotFoundError:
            payload = {"message": "failed","error": "Not found"}
            return make_response(jsonify(payload), 404)
