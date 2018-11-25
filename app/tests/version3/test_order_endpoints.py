from flask import current_app
from unittest import TestCase

from app import create_app
from app.db_config import destroy_tables


class TestParcelUserOrderEndpoints(TestCase):
 
    def setUp(self):
        self.app = create_app('testing')
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        destroy_tables('parcels', 'users')
        self.app_context.pop()
