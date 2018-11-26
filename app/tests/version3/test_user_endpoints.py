import json
from unittest import TestCase

import psycopg2
import pytest


from app import create_app
from app.api.version3.models.users import NORMAL, ADMIN
from app.db_config import create_tables, destroy_tables


class TestUnauthenticatedUserEndpoints(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        create_tables()
        self.client = self.app.test_client()
        self.signup_data = {"name": "bob",
                            "email": "bob@email.com",
                            "password": "burgers"
                           }
        self.admin_signup_data = {
            "name": "linda",
            "email": "linda@email.com",
            "password": "linda",
            "role": ADMIN
        }

        self.user_data = {
            "id": 1,
            "name": "bob",
            "email": "bob@email.com",
        }
        self.login_data = {
            "email": "bob@email.com",
            "password": "burgers"
        }
        self.admin_login_data = {
            "email": "linda@email.com",
            "password": "linda"
        }

    def tearDown(self):
        destroy_tables("users", "parcels")
        self.app_context.pop()

    def test_signing_up_a_new_user(self):
        with self.client:
            response = self.client.post("/api/v3/auth/signup",
                                        data=json.dumps(self.signup_data),
                                        content_type="application/json")
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(response_data["message"], "Success")
            self.assertTrue(response_data["user"], self.user_data)

            # create account with an existing email address
            response2 = self.client.post("/api/v3/auth/signup",
                                        data=json.dumps(self.signup_data),
                                        content_type="application/json")
            response2_data = json.loads(response2.data.decode())
            self.assertEqual(response2.status_code, 400)
            self.assertEqual(response2_data["message"],
                             "Sorry, your email is already taken")
            self.assertEqual(response2_data["error"],
                             "Email not unique")
            
            # test signing up an admin user
            response3 = self.client.post("/api/v3/auth/signup",
                                        data=json.dumps(self.admin_signup_data),
                                        content_type="application/json")
            response3_data = json.loads(response3.data.decode())
            self.assertEqual(response3.status_code, 201)
            self.assertTrue(response3_data["message"], "Success")
            self.assertTrue(response3_data["user"]["role"], ADMIN)

    def test_logging_in_a_user(self):
        with self.client:
            intial_response = self.client.post("/api/v3/auth/signup",
                                               data=json.dumps(self.signup_data),
                                               content_type="application/json")
            response = self.client.post("/api/v3/auth/login",
                                        data=json.dumps(self.login_data),
                                        content_type="application/json")
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response_data["message"], "Success")
            self.assertTrue(response_data["user"], self.user_data)
            self.assertIsNotNone(response_data["access_token"])

            # logging in with non existing email address
            response2 = self.client.post("/api/v3/auth/login",
                                         data=json.dumps(dict(
                                             email="bobby@email.com",
                                             password="burgers")
                                         ),
                                         content_type="application/json")
            response2_data = json.loads(response2.data.decode())
            self.assertEqual(response2.status_code, 404)
            self.assertTrue(response2_data["message"], "Sorry, we cannot find such a user")
            self.assertTrue(response2_data["error"], "User not found")

            # loggin in with wrong password
            response3 = self.client.post("/api/v3/auth/login",
                                         data=json.dumps(dict(
                                            email="bob@email.com",
                                            password="burger")
                                         ),
                                         content_type="application/json")
            response3_data = json.loads(response3.data.decode())
            self.assertEqual(response3.status_code, 400)
            self.assertTrue(response3_data["message"], "Sorry, your password is incorrect")
            self.assertTrue(response3_data["error"], "Incorrect password")
