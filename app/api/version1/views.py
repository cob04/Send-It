# views.py

from flask import jsonify, make_response, request, jsonify
from flask_restful import Resource

from .models import ParcelOrderStore

parcel_orders = []


class ParcelOrderList(Resource):

    def __init__(self):
        self.store = ParcelOrderStore()

    def get(self):
        parcels = self.store.all()
        return make_response(jsonify(parcels), 200)

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
