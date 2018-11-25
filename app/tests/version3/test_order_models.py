from flask import current_app

from unittest import TestCase

import psycopg2
import pytest


from app import create_app
from app.api.version3.models.orders import ParcelOrderModel, ParcelOrderManager
from app.db_config import create_tables, destroy_tables


class ParcelOrderModelTests(TestCase):

    def test_initializing_a_parcel(self):
        parcel = ParcelOrderModel(1, "bob", "linda", "home", "restaurant", 2)
        self.assertEqual(parcel.sender, "bob")
        self.assertEqual(parcel.recipient, "linda")
        self.assertEqual(parcel.pickup, "home")
        self.assertEqual(parcel.destination, "restaurant")
        self.assertEqual(parcel.weight, 2)

    def test_parcel_object_presentation(self):
        parcel = ParcelOrderModel(1, "bob", "linda", "home", "restaurant", 2)
        self.assertEqual(repr(parcel),
                         "Parcel(bob, linda, home, restaurant, 2Kg)")

    def test_parcel_in_dictionary_format(self):
        parcel = ParcelOrderModel(1, "bob", "linda", "home", "restaurant", 2)
        parcel_dict = {
            "user_id": 1,
            "sender": "bob",
            "recipient": "linda",
            "pickup": "home",
            "destination": "restaurant",
            "present_location": "home",
            "weight": 2.0,
            "status": "Parcel not delivered"
        }
        self.assertEqual(parcel.to_dict(), parcel_dict)


class TestParcelOrderManager(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        create_tables()

    def tearDown(self):
        destroy_tables('parcels')
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_inserting_parcels_into_database(self):
        manager = ParcelOrderManager()
        parcel = ParcelOrderModel(1, "bob", "linda", "home", "restaurant", 4)
        result = manager.save(parcel)
        self.assertEqual(result, parcel)

    def test_fetching_all_parcesls_from_the_db(self):
        parcel1 = ParcelOrderModel(1, "bob", "linda", "home", "restaurant", 2)
        parcel2 = ParcelOrderModel(1, "gin", "louiz", "home", "restaurant", 3)
        manager = ParcelOrderManager()
        manager.save(parcel1)
        manager.save(parcel2)
        parcel1.id = 1
        parcel2.id = 2
        self.assertEqual(manager.fetch_all(), [parcel1, parcel2])
