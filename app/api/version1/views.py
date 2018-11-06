# views.py

from flask import jsonify, make_response, request, jsonify
from flask_restful import Resource



parcel_orders = []


class ParcelOrderList(Resource):

    def get(self):
        payload = {"message": "success",
                "parcel orders": parcel_orders }
        return make_response(jsonify(payload), 200)

    def post(self):
        request_data = request.get_json()
        sender = request_data['sender']
        recipient = request_data['recipient']
        phone = request_data['phone']
        pickup = request_data['pickup']
        destination = request_data['destination']
        weight = request_data['weight']

        payload = {
            "id": len(parcel_orders) + 1,
            "sender": sender,
            "recipient": recipient,
            "pickup": pickup,
            "destination": destination,
            "weight": weight
        }

        parcel_orders.append(payload)

        return make_response(jsonify(payload), 201)
