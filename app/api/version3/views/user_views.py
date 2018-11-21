# views.py
from flask_restful import reqparse, Resource
from flask_jwt_extended import create_access_token

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
            "user": user.to_dict()
        }
        return payload, 201


class UserSignup(Resource):

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


class UserLogin(Resource):

    def __init__(self):
        self.manager = UserManager()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True,
                            help="To login you need an email")
        parser.add_argument('password', type=str, required=True,
                            help="To login you need a password")

        args = parser.parse_args()
        email, password = args['email'], args["password"]
        status, content = self.manager.authenticate(email, password)
        if status:
            access_token = create_access_token(identity=email)
            payload = {
                "message": "Success",
                "user": content.to_dict(),
                "access_token": access_token
            }
            return payload, 200
        else:
            payload = {
                "message": "We were unable to log you in",
                "error": str(content),
            }
            return payload, 404
