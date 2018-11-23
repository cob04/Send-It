from unittest import TestCase
import psycopg2
import pytest

from app import create_app
from app.api.version3.models.orders import ParcelOrderModel, ParcelOrderManager
from app.db_config import create_tables, destroy_tables


url = "dbname='sendit' host='localhost' port='5432' user='eric' 'password='hardpassword'"


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


class TestParcelOrderManager:
    
    def test_inserting_parcels_into_database(self, init_db):
        manager = ParcelOrderManager()
        parcel = ParcelOrderModel(1, "bob", "linda", "home", "restaurant", 2)
        info = manager.save(parcel)
        assert info == parcel
        destroy_tables('parcels')

"""    
    def test_fetching_all_parcesls_from_the_db(self, init_db):
        parcel1 = ParcelOrderModel(1, "bob", "linda", "home", "restaurant", 2)
        parcel2 = ParcelOrderModel(1, "gin", "louiz", "home", "restaurant", 2)
        manager = ParcelOrderManager()
        manager.save(parcel1)
        manager.save(parcel2)
        print(manager.fetch_all())
        assert manager.fetch_all() == [parcel1, parcel2]
        destroy_tables('parcels')
"""
