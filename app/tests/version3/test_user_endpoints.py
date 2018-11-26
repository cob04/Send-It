import json
from unittest import TestCase

import psycopg2
import pytest


from app import create_app
from app.api.version3.models.users import NORMAL, ADMIN
from app.db_config import create_tables, destroy_tables


class TestUserManager(TestCase):

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
        self.user_data = {
            "id": 1,
            "name": "bob",
            "email": "bob@email.com",
            "role": NORMAL
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
