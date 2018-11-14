# test_order_endpoints.py

import json
import unittest

from app import create_app

from ..models import NOT_DELIVERED


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
