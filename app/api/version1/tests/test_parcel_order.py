import unittest
import json

from app import create_app


class TestDataParcel(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()
