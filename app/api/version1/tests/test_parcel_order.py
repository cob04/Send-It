import unittest
import json

from app import create_app


class TestParcelOrderList(unittest.TestCase):

    def setUp(self):
        create_app().testing = True
        self.app = create_app().test_client()
        self.data = {
            "sender": "bob",
            "recipient": "linda",
            "pickup": "home",
            "destination": "restaurant",
            "weight": "2kg"
        }

    def test_post(self):
        response = self.app.post('/api/v1/parcels',
                                  data=json.dumps(self.data),
                                  content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_get(self):
        response = self.app.get('/api/v1/parcels')
        self.assertEqual(response.status_code, 200)


class TestParcelOrder(unittest.TestCase):

    def setUp(self):
        create_app().testing = True
        self.app = create_app().test_client()
        self.data = {
            "sender": "bob",
            "recipient": "linda",
            "pickup": "home",
            "destination": "restaurant",
            "weight": "2kg"
        }

    def test_get_by_id_when_order_exists(self):
        response = self.app.get('/api/v1/parcels/1')
        self.assertEqual(response.status_code, 200)

    def test_get_by_id_when_order_does_not_exist(self):
        response = self.app.get('/api/v1/parcels/2')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
