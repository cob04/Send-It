from flask import current_app

from unittest import TestCase

import psycopg2
import pytest


from app import create_app
from app.api.version3.exceptions import ParcelNotFoundError
from app.api.version3.models.orders import ParcelOrderModel, ParcelOrderManager
from app.api.version3.models.orders import CANCELLED, DELIVERED
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
            "status": "Not delivered"
        }
        self.assertEqual(parcel.to_dict(), parcel_dict)


class TestParcelOrderManager(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        create_tables()
        self.manager = ParcelOrderManager()

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

    def test_fetching_one_parcel(self):
        parcel = ParcelOrderModel(1, "bob", "linda", "home", "restaurant", 2)
        self.manager.save(parcel)
        parcel.id = 1
        self.assertEqual(self.manager.fetch_by_id(1), parcel)
        # test fetching a parcel that does not exist
        with self.assertRaises(ParcelNotFoundError):
            self.manager.fetch_by_id(2)

    def test_parcels_owned_by_one_user(self):
        parcel1 = ParcelOrderModel(1, "bob", "linda", "home", "restaurant", 4)
        parcel2 = ParcelOrderModel(2, "bob", "linda", "home", "restaurant", 2)
        parcel3 = ParcelOrderModel(1, "bob", "linda", "home", "restaurant", 6)
        parcel1.id = 1
        parcel2.id = 2
        parcel3.id = 3
        self.manager.save(parcel1)
        self.manager.save(parcel2)
        self.manager.save(parcel3)
        self.assertEqual(self.manager.fetch_all_user_parcels(1), [parcel1, parcel3])

    def test_cancelling_a_parcel(self):
        parcel1 = ParcelOrderModel(1, "bob", "linda", "home", "restaurant", 4)
        self.manager.save(parcel1)
        parcel1.id = 1
        parcel1.status = CANCELLED
        self.assertEqual(self.manager.cancel_by_id(1), parcel1)
        # test cancelling a parcel that doesn't exist
        with self.assertRaises(ParcelNotFoundError):
            self.manager.cancel_by_id(3)

    def test_updating_parcel_destination(self):
        parcel1 = ParcelOrderModel(1, "bob", "linda", "home", "restaurant", 4)
        self.manager.save(parcel1)
        parcel1.id = 1
        self.assertEqual(self.manager.update_destination(1, "Nairobi").destination,
                         "Nairobi")
        # test changing destination for a parcel that does'nt exist
        with self.assertRaises(ParcelNotFoundError):
            self.manager.update_destination(4, "Nairobi")

    def test_updating_parcel_status(self):
        parcel1 = ParcelOrderModel(1, "bob", "linda", "home", "restaurant", 4)
        self.manager.save(parcel1)
        parcel1.id = 1
        self.assertEqual(self.manager.update_status(1, DELIVERED).status,
                         DELIVERED)
        # test changing the status for a parcel that does'nt exist
        with self.assertRaises(ParcelNotFoundError):
            self.manager.update_status(6, DELIVERED)
    
    def test_updating_parcel_present_location(self):
        parcel1 = ParcelOrderModel(1, "bob", "linda", "home", "restaurant", 4)
        self.manager.save(parcel1)
        parcel1.id = 1
        self.assertEqual(self.manager.update_present_location(1, "Kisumu").present_location,
                         "Kisumu")
        # test changing present location for a parcel that does'nt exist
        with self.assertRaises(ParcelNotFoundError):
            self.manager.update_present_location(2, "Kisumu")

