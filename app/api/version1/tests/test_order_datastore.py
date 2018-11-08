# test_datastore.py

import unittest

from ..models import ParcelOrderStore
from ..models import NOT_DELIVERED


class ParcelOrderStoreTests(unittest.TestCase):

    def setUp(self):
        self.store = ParcelOrderStore()

    def tearDown(self):
        self.store.db.clear()

    def test_adding_order_to_store(self):
        payload = self.store.save('bob', 'linda', 'home', 'restaurant', '1kg')
        self.assertEqual(payload, {'id': 1,
                                   'sender': 'bob',
                                   'recipient': 'linda',
                                   'pickup': 'home',
                                   'destination': 'restaurant',
                                   'weight': '1kg',
                                   'status': NOT_DELIVERED})
        self.assertEqual(self.store.db, [payload])
