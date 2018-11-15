# test_user_endpoints.py

import json
import unittest

from app import create_app

from app.api.version1.models import NOT_DELIVERED
from app.api.version1.models import parcel_orders


class ParcelOrderEnpointsTests(unittest.TestCase):

    def setUp(self):
        create_app().testing = True
        self.app = create_app().test_client()
        self.data = {
            "user_id": 1,
            "sender": "bob",
            "recipient": "linda",
            "pickup": "home",
            "destination": "restaurant",
            "weight": "2kg"}

    def tearDown(self):
        parcel_orders.clear()

    def test_fetching_orders_by_user_id(self):
        self.app.post('/api/v1/parcels',
                      data=json.dumps(self.data),
                      content_type="application/json")
        response = self.app.get('/api/v1/users/1/parcels')
        self.assertEqual(response.status_code, 200)
        expected_json = {
            "message": "Success",
            "parcel_orders": [{
                "id": 1,
                "user_id": 1,
                "sender": "bob",
                "recipient": "linda",
                "pickup": "home",
                "destination": "restaurant",
                "weight": "2kg",
                "status": NOT_DELIVERED}]}
        self.assertEqual(expected_json, response.get_json())

    def test_fetching_orders_by_user_id_with_unexistant_id(self):
        self.app.post('/api/v1/parcels',
                      data=json.dumps(self.data),
                      content_type="application/json")
        test_user_id = 3
        response = self.app.get('/api/v1/users/%d/parcels' % test_user_id)
        self.assertEqual(response.status_code, 404)
        expected_json = {
            "message": "Sorry, we cannot find a user with"
                       " the id %d" % test_user_id,
            "error": "User Not Found"
        }
        self.assertEqual(expected_json, response.get_json())


class UserAccountTests(unittest.TestCase):

    def setUp(self):
        create_app().testing = True
        self.app = create_app().test_client()
        self.data = {
            "name": "bob",
            "email": "bob@email.com",
            "password": "burgers",
        }

    def test_adding_a_new_user(self):
        response = self.app.post('/api/v2/users',
                                 data=json.dumps(self.data),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 201)
        data = self.data
        data["id"] = 1
        expected_json = {
            "message": "success",
            "user": data
        }
        self.assertEqual(response.get_json, expected_json)
