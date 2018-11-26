import json

from unittest import TestCase

from app import create_app
from app.api.version3.models.orders import (NOT_DELIVERED, CANCELLED,
                                            IN_TRANSIT)
from app.api.version3.models.users import ADMIN
from app.db_config import create_tables, destroy_tables


class TestAuthenticatedOrderEndpoints(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        create_tables()
        self.client = self.app.test_client()
        self.signup_info = {"name": "bob",
                            "email": "bob@email.com",
                            "password": "burgers"
                           }
        self.admin_signup_info = {"name": "linda",
                                  "email": "linda@email.com",
                                  "password": "linda",
                                  "role": ADMIN
                                 }
        self.login_info = {
            "email": "bob@email.com",
            "password": "burgers"
        }
        self.admin_login_info = {
            "email": "linda@email.com",
            "password": "linda"
        }
        self.parcel_data = {
            "sender": "bob",
            "recipient": "linda",
            "pickup": "home",
            "destination": "restaurant",
            "weight": 2
        }
        self.order_response = {
                "id": 1,
                "user_id": 1,
                "sender": "bob",
                "recipient": "linda",
                "pickup": "home",
                "destination": "restaurant",
                "present_location": "home",
                "weight": 2.0,
                "status": NOT_DELIVERED
        }
        with self.client:
            self.client.post("/api/v3/auth/signup",
                             data=json.dumps(self.signup_info),
                             content_type="application/json")
            self.client.post("/api/v3/auth/signup",
                             data=json.dumps(self.admin_signup_info),
                             content_type="application/json")
            # get normal user token
            response = self.client.post("/api/v3/auth/login",
                             data=json.dumps(self.login_info),
                             content_type="application/json")
            self.login_data = response.data.decode()
            self.auth_token = "Bearer " + json.loads(self.login_data)['access_token']
            # get normal admin user token
            admin_response = self.client.post("/api/v3/auth/login",
                                              data=json.dumps(self.admin_login_info),
                                              content_type="application/json")
            self.admin_login_data = admin_response.data.decode()
            self.admin_auth_token = "Bearer " + json.loads(self.admin_login_data)['access_token']

    def tearDown(self):
        destroy_tables("users", "parcels")
        self.app_context.pop()

    def test_parcels_endpoint_post_and_get_requests(self):
        with self.client:
            # posting a new parcel
            response = self.client.post(
                "/api/v3/parcels",
                data=json.dumps(self.parcel_data),
                headers=dict(Authorization=self.auth_token),
                content_type="application/json")
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response_data["message"], "Success")

            # getting all parcels
            response2 = self.client.get(
                "/api/v3/parcels",
                headers=dict(Authorization=self.auth_token))
            response2_data = json.loads(response2.data.decode())
            self.assertEqual(response2.status_code, 200)
            self.assertEqual(response2_data["message"], "Success")
            self.assertEqual(response2_data["parcel_orders"], [self.order_response])

            # admin getting all parcels
            response3 = self.client.get(
                "/api/v3/parcels",
                headers=dict(Authorization=self.admin_auth_token))
            response3_data = json.loads(response3.data.decode())
            self.assertEqual(response3.status_code, 200)
            self.assertEqual(response3_data["message"], "Success")
            self.assertEqual(response3_data["parcel_orders"], [self.order_response])

    def test_fetching_a_parcel_order(self):
         with self.client:
            # posting a new parcel
            self.client.post(
                "/api/v3/parcels",
                data=json.dumps(self.parcel_data),
                headers=dict(Authorization=self.auth_token),
                content_type="application/json")

            # getting all parcels
            response = self.client.get(
                "/api/v3/parcels/1",
                headers=dict(Authorization=self.auth_token))
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_data["message"], "Success")
            self.assertEqual(response_data["parcel_order"], self.order_response)

    def test_cancelling_an_parcel_order(self):
         with self.client:
            # posting a new parcel
            self.client.post(
                "/api/v3/parcels",
                data=json.dumps(self.parcel_data),
                headers=dict(Authorization=self.auth_token),
                content_type="application/json")

            # getting all parcels
            response = self.client.put(
                "/api/v3/parcels/1/cancel",
                headers=dict(Authorization=self.auth_token))
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response_data["message"], "Success")
            self.assertEqual(response_data["parcel_order"]["status"], CANCELLED)

    def test_updating_parcel_order_status(self):
         with self.client:
            # posting a new parcel
            self.client.post(
                "/api/v3/parcels",
                data=json.dumps(self.parcel_data),
                headers=dict(Authorization=self.auth_token),
                content_type="application/json")

            # test using normal user
            response2 = self.client.put(
                "/api/v3/parcels/1/status",
                data=json.dumps(dict(status=IN_TRANSIT)),
                headers=dict(Authorization=self.auth_token),
                content_type="application/json")
            response2_data = json.loads(response2.data.decode())
            self.assertEqual(response2.status_code, 401)
            self.assertEqual(response2_data["message"], "Sorry, you are unauthorized")

    def test_updating_parcel_order_destination(self):
         with self.client:
            # posting a new parcel
            self.client.post(
                "/api/v3/parcels",
                data=json.dumps(self.parcel_data),
                headers=dict(Authorization=self.auth_token),
                content_type="application/json")

            # test using normal user
            response2 = self.client.put(
                "/api/v3/parcels/1/destination",
                data=json.dumps(dict(destination="Nairobi")),
                headers=dict(Authorization=self.auth_token),
                content_type="application/json")
            response2_data = json.loads(response2.data.decode())
            self.assertEqual(response2.status_code, 201)
            self.assertEqual(response2_data["message"], "Success")
            self.assertEqual(response2_data["parcel_order"]["destination"],
                             "Nairobi")

    def test_updating_parcel_present_location(self):
         with self.client:
            # post a new parcel
            self.client.post(
                "/api/v3/parcels",
                data=json.dumps(self.parcel_data),
                headers=dict(Authorization=self.auth_token),
                content_type="application/json")

            # test using normal user
            response2 = self.client.put(
                "/api/v3/parcels/1/presentLocation",
                data=json.dumps(dict(present_location="Kisumu")),
                headers=dict(Authorization=self.auth_token),
                content_type="application/json")
            response2_data = json.loads(response2.data.decode())
            self.assertEqual(response2.status_code, 401)
            self.assertEqual(response2_data["message"], "Sorry, you are unauthorized")
