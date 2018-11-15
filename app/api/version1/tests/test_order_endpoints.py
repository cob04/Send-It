# test_order_endpoints.py

import json
import unittest

from app import create_app

from ..models import CANCELLED, NOT_DELIVERED, IN_TRANSIT
from ..models import parcel_orders


class ParcelOrderEndpointsTests(unittest.TestCase):

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

    def test_post_new_parcel_delivery_order(self):
        response = self.app.post('/api/v1/parcels',
                                 data=json.dumps(self.data),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 201)
        expected_json = {
            "message": "Success",
            "parcel_order": {
                "id": 1,
                "user_id": 1,
                "sender": "bob",
                "recipient": "linda",
                "pickup": "home",
                "destination": "restaurant",
                "weight": "2kg",
                "status": NOT_DELIVERED}}
        self.assertEqual(response.get_json(), expected_json)

    def test_post_new_parcel_validation_with_defective_data(self):
        defective_data = {
            "user_id": "my id is 1",
            "sender": "bob",
            "recipient": "linda",
            "pickup": "home",
            "destination": "restaurant",
            "weight": 2
        }
        response = self.app.post('/api/v1/parcels',
                                 data=json.dumps(defective_data),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)
        expected_json = {
            "message": {
                "user_id": "Order must have an integer user id"
            }
        }
        self.assertEqual(response.get_json(), expected_json)

    def test_get_all_parcel_delivery_orders(self):
        self.app.post('/api/v1/parcels',
                      data=json.dumps(self.data),
                      content_type="application/json")
        response = self.app.get('/api/v1/parcels')
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
        self.assertEqual(response.get_json(), expected_json)

    def test_get_by_id_when_order_exists(self):
        self.app.post('/api/v1/parcels',
                      data=json.dumps(self.data),
                      content_type="application/json")
        response = self.app.get('/api/v1/parcels/1')
        self.assertEqual(response.status_code, 200)
        expected_json = {
            "message": "Success",
            "parcel_order": {
                "id": 1,
                "user_id": 1,
                "sender": "bob",
                "recipient": "linda",
                "pickup": "home",
                "destination": "restaurant",
                "weight": "2kg",
                "status": NOT_DELIVERED}}
        self.assertEqual(response.get_json(), expected_json)

    def test_get_by_id_when_order_does_not_exist(self):
        response = self.app.get('/api/v1/parcels/2')
        self.assertEqual(response.status_code, 404)
        expected_json = {
            "message": "Sorry, we cannot find such an order",
            "error": "Not found"
        }
        self.assertEqual(response.get_json(), expected_json)

    def test_cancelling_an_order(self):
        post_response = self.app.post('/api/v1/parcels',
                                      data=json.dumps(self.data),
                                      content_type="application/json")
        self.assertEqual(post_response.status_code, 201)
        data = {
            "status": CANCELLED
        }

        put_response = self.app.put('/api/v1/parcels/1/cancel',
                                    data=json.dumps(data),
                                    content_type="application/json")
        data["id"] = 1
        expected_json = {
            "message": "Success",
            "parcel_order": {
                "id": 1,
                "user_id": 1,
                "sender": "bob",
                "recipient": "linda",
                "pickup": "home",
                "destination": "restaurant",
                "weight": "2kg",
                "status": CANCELLED
            }
        }
        self.assertEqual(put_response.status_code, 201)
        self.assertEqual(put_response.get_json(), expected_json)

    def test_cancelling_an_order_with_status_not_cancelled(self):
        post_response = self.app.post('/api/v1/parcels',
                                      data=json.dumps(self.data),
                                      content_type="application/json")
        self.assertEqual(post_response.status_code, 201)
        data = {
            "status": IN_TRANSIT
        }

        put_response = self.app.put('/api/v1/parcels/1/cancel',
                                    data=json.dumps(data),
                                    content_type="application/json")
        expected_json = {
            "message": "Please set status field to %s" % CANCELLED,
            "error": "Invalid field entry"
        }
        self.assertEqual(put_response.status_code, 400)
        self.assertEqual(put_response.get_json(), expected_json)

    def test_cancelling_an_order_with_wrong_order_id(self):
        post_response = self.app.post('/api/v1/parcels',
                                      data=json.dumps(self.data),
                                      content_type="application/json")
        self.assertEqual(post_response.status_code, 201)
        data = {
            "status": CANCELLED
        }

        put_response = self.app.put('/api/v1/parcels/3/cancel',
                                    data=json.dumps(data),
                                    content_type="application/json")
        data["id"] = 1
        expected_json = {
            "message": "Sorry, we cannot find that order",
            "error": "Not found"
        }
        self.assertEqual(put_response.status_code, 404)
        self.assertEqual(put_response.get_json(), expected_json)
