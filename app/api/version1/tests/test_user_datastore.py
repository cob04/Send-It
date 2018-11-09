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
