# views.py
from flask_restful import reqparse, Resource

from ..models.users import UserModel, UserManager


class UserList(Resource):

    def __init__(self):
        self.manager = UserManager()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="User must have a name")
        parser.add_argument('email', type=str, required=True,
                            help="User must have a email")
        parser.add_argument('password', type=str, required=True,
                            help="User must have a password")

        args = parser.parse_args()

        user = UserModel(**args)
        self.manager.save(user)
        payload = {
            "message": "Success",
            "user_user": user.to_dict()
        }
        return payload, 201


class User(Resource):

    def __init__(self):
        self.manager = UserManager()

    def get(self, user_id):
        user = self.manager.fetch_by_id(user_id)
        if user:
            payload = {
                "message": "Success",
                "user": user.to_dict()
            }
            return payload, 200
        else:
            payload = {
                "message": "Sorry, we cannot find such a user",
                "error": "Not found"
            }
