# test_datastore.py

import unittest

from ..models import ParcelOrderStore
from ..models import CANCELLED, NOT_DELIVERED


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

    def test_fetching_orders_in_the_store(self):
        self.store.save('bob', 'linda', 'home', 'restaurant', '1kg')
        self.assertEqual(self.store.all(),
                         [{'id': 1,
                           'sender': 'bob',
                           'recipient': 'linda',
                           'pickup': 'home',
                           'destination': 'restaurant',
                           'weight': '1kg',
                           'status': NOT_DELIVERED}])

    def test_fetching_order_by_id(self):
        self.store.save('bob', 'linda', 'home', 'restaurant', '1kg')
        self.assertEqual(self.store.fetch_by_id(1),
                         {'id': 1,
                          'sender': 'bob',
                          'recipient': 'linda',
                          'pickup': 'home',
                          'destination': 'restaurant',
                          'weight': '1kg',
                          'status': NOT_DELIVERED})

    def test_fetching_non_existant_order_by_id(self):
        store = ParcelOrderStore()
        with self.assertRaises(IndexError):
            store.fetch_by_id(1)

    def test_marking_order_as_cancelled(self):
        self.store.save('bob', 'linda', 'home', 'restaurant', '1kg')
        self.assertEqual(self.store.cancel_by_id(1),
                         {'id': 1,
                          'sender': 'bob',
                          'recipient': 'linda',
                          'pickup': 'home',
                          'destination': 'restaurant',
                          'weight': '1kg',
                          'status': CANCELLED})
