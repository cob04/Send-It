from unittest import TestCase
import psycopg2

from app import create_app
from app.api.version3.models.orders import ParcelOrderModel, ParcelOrderManager
from app.db_config import create_tables, destroy_tables


url = "dbname='sendit' host='localhost' port='5432' user='eric' 'password='hardpassword'"


class ParcelOrderModelTests(TestCase):

    def test_initializing_a_parcel(self):
        parcel = ParcelOrderModel("bob", "linda", "home", "restaurant", 2)
        self.assertEqual(parcel.sender, "bob")
        self.assertEqual(parcel.recipient, "linda")
        self.assertEqual(parcel.pickup, "home")
        self.assertEqual(parcel.destination, "restaurant")
        self.assertEqual(parcel.weight, 2)

    def test_parcel_object_presentation(self):
        parcel = ParcelOrderModel("bob", "linda", "home", "restaurant", 2)
        self.assertEqual(repr(parcel),
                         "Parcel(bob, linda, home, restaurant, 2Kg)")


class ParcelOrderManagerTests(TestCase):

    def setUp(self):
        self.app = create_app()

    def tearDown(self):
        destroy_tables("parcels")

    def test_inserting_parcels_into_database(self):
        manager = ParcelOrderManager()
        parcel = ParcelOrderModel("bob", "linda", "home", "restaurant", 2)
        info = manager.save(parcel)
        self.assertEqual(info, "Successfully inserted new parcel")

    def test_fetching_all_parcesls_from_the_db(self):
        parcel1 = ParcelOrderModel("bob", "linda", "home", "restaurant", 2)
        parcel2 = ParcelOrderModel("gin", "louiz", "home", "restaurant", 2)
        manager = ParcelOrderManager()
        manager.save(parcel1)
        manager.save(parcel2)
        self.assertEqual(manager.fetch_all(), [parcel1, parcel2])
