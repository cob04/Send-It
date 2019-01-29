# views.py
from flask_restful import reqparse, Resource
from flask_jwt_extended import create_access_token

from ..exceptions import (UserNotFoundError, ApplicationError,
                          IncorrectPasswordError, EmailNotUniqueError)
from ..models.users import UserModel, UserManager


class UserSignup(Resource):
    """Resource that provides sigb endpoint for user
    account creation.
    """
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
        parser.add_argument("role", type=str, required=False,
                            help="User role Normal or Administrator")
        args = parser.parse_args()

        user = UserModel(**args)
        try:
            self.manager.save(user)
            payload = {
                "message": "Success",
                "user": user.to_dict()
            }
            return payload, 201

        except EmailNotUniqueError:
            payload = {
                "message": "Sorry, your email is already taken",
                "error": "Email not unique"
            }
            return payload, 400

        except ApplicationError:
            payload = {
                "messsage": "Sorry, something has gone terribly wrong",
                "error": "Application error"
            }
            return payload, 500


class UserLogin(Resource):
    """Resource that provides endpoint to login users."""
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
        try:
            user = self.manager.authenticate(email, password)
            access_token = create_access_token(identity=user.id,
                                               expires_delta=False)
            payload = {
                "message": "Success",
                "user": user.to_dict(),
                "access_token": access_token
            }
            return payload, 200
        except UserNotFoundError:
            payload = {
                "message": "Sorry, we cannot find such a user",
                "error": "User not found"
            }
            return payload, 404
        except IncorrectPasswordError:
            payload = {
                "message": "Sorry, your password is incorrect",
                "error": "Incorrect password"
            }
            return payload, 400
        except ApplicationError:
            payload = {
                "message": "Sorry, something went wrong. we are fixing it"
            }
            return payload, 500
