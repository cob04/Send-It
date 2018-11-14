# test_order_endpoints.py

import json
import unittest

from app import create_app

from ..models import NOT_DELIVERED
from ..models import parcel_orders


class ParcelOrderEnpointsTests(unittest.TestCase):

    def setUp(self):
        create_app().testing = True
        self.app = create_app().test_client()
        self.data = {
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
            "message": "success",
            "parcel_order": {
                "id": 1,
                "sender": "bob",
                "recipient": "linda",
                "pickup": "home",
                "destination": "restaurant",
                "weight": "2kg",
                "status": NOT_DELIVERED}}
        self.assertEqual(response.get_json(), expected_json)

    def test_get_all_parcel_delivery_orders(self):
        self.app.post('/api/v1/parcels',
                      data=json.dumps(self.data),
                      content_type="application/json")
        response = self.app.get('/api/v1/parcels')
        self.assertEqual(response.status_code, 200)
        expected_json = {
            "message": "success",
            "parcel_orders": [{
                "id": 1,
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
            "message": "success",
            "parcel_order": {
                "id": 1,
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
        expected_json = {"message": "failed", "error": "Not found"}
        self.assertEqual(response.get_json(), expected_json)
