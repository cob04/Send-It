import unittest

from ..models import ParcelOrderStore
from ..exceptions import OrderNotFoundError


class ParcelOrderStoreTests(unittest.TestCase):

    def setUp(self):
        self.store = ParcelOrderStore()

    def test_adding_order_to_store(self):
        payload = self.store.save('bob', 'linda', 'home', 'restaurant', '1kg')
        self.assertEqual(payload, {'id': 1,
                                   'sender': 'bob',
                                   'recipient': 'linda',
                                   'pickup': 'home',
                                   'destination': 'restaurant',
                                   'weight': '1kg'})
        self.assertEqual(self.store.db, [payload])

    def test_fetching_orders_in_the_store(self):
         self.assertEqual(self.store.all(),
                          [{'id': 1,
                            'sender': 'bob',
                            'recipient': 'linda',
                            'pickup': 'home',
                            'destination': 'restaurant',
                            'weight': '1kg'
                           }])

    def test_fetching_order_by_id(self):
        self.assertEqual(self.store.fetch_by_id(1),
                         {'id': 1,
                          'sender': 'bob',
                          'recipient': 'linda',
                          'pickup': 'home',
                          'destination': 'restaurant',
                          'weight': '1kg'
                        })

    def test_fetching_by_id_from_an_empty_store(self):
        store = ParcelOrderStore()
        store.db = []
        with self.assertRaises(OrderNotFoundError) as e:
            store.fetch_by_id(1)
