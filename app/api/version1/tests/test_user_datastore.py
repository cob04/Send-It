# test_user_datastore.py

import unittest

from ..models import UserDataStore


class UserDataStoreTests(unittest.TestCase):

    def setUp(self):
        self.store = UserDataStore()

    def tearDown(self):
        self.store.db.clear()

    def test_adding_order_to_store(self):
        payload = self.store.save('bob', 'bob@email.com', 'burgers')
        self.assertEqual(payload, {'id': 1,
                                   'name': 'bob',
                                   'email': 'bob@email.com'})

    def test_authenticating_a_user(self):
        self.store.save('bob', 'bob@gmail.com', 'burgers')
        self.assertTrue(self.store.authenticate("bob@gmail.com", "burgers"))
        self.assertFalse(self.store.authenticate("bob@gmail.com", "banana"))
        self.assertFalse(self.store.authenticate("bob", "burgers"))

    def test_fetching_a_user_by_id(self):
        self.store.save('bob', 'bob@email.com', 'burgers')
        payload = self.store.fetch_by_id(1)
        expected_json = {
            "id": 1,
            "name": "bob",
            "email": "bob@email.com"
        }
        self.assertEqual(payload, expected_json)
