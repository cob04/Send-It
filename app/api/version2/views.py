# views.py

from flask import jsonify, make_response
from flask_restful import reqparse, Resource

from .models import CANCELLED
from .models import ParcelOrderStore, UserDataStore


class ParcelOrderList(Resource, ParcelOrderStore):

    def __init__(self):
        self.store = ParcelOrderStore()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True,
                            help="Order must have an integer user id")
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

        user_id = args["user_id"]
        sender = args["sender"]
        recipient = args["recipient"]
        pickup = args["pickup"]
        destination = args["destination"]
        weight = args["weight"]

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
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=True,
                            help="You must have a status")
        args = parser.parse_args()
        status = args["status"]
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
        # check if user id exists, because we don't have
        # a user store lets check if the user_id can be
        # found in any of the orders.
        user_ids = set([order['user_id'] for order in self.store.all()])
        if user_id in user_ids:
            order = self.store.fetch_by_user_id(user_id)
            payload = {
                "message": "Success",
                "parcel_orders": order
            }
            return make_response(jsonify(payload), 200)
        else:
            payload = {
                "message": "Sorry, we cannot find a user"
                           " with the id %d" % user_id,
                "error": "User Not Found"
            }
            return make_response(jsonify(payload), 404)


class UserList(Resource, UserDataStore):

    def __init__(self):
        self.store = UserDataStore()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="A user must have a name")
        parser.add_argument('email', type=str, required=True,
                            help="A user must have an email address")
        parser.add_argument('password', type=str, required=True,
                            help="A user must have a password")

        args = parser.parse_args()

        name = args["name"]
        email = args["email"]
        password = args["password"]

        new_user = self.store.save(name, email, password)
        payload = {
            "message": "Success",
            "user": new_user
        }
        return make_response(jsonify(payload), 201)

class AuthLogin(Resource, UserDataStore):

    def __init__(self):
        self.store = UserDataStore()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True,
                            help="Email address is required")
        parser.add_argument('password', type=str, required=True,
                            help="Password is required")

        args = parser.parse_args()

        email = args["email"]
        password = args["password"]
        
        login_info = self.store.login_user(email, password)
        if "error" in set(login_info.keys()):
            payload = {
                "message": "Your email or password is invalid",
                "error": "Invalid credentials",
            }
            return make_response(jsonify(payload), 400)
        else:
            payload = {
                "message": "Success",
                "user": login_info,
            }
            return make_response(jsonify(payload), 200)
