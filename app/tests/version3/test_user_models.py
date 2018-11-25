from flask import current_app

from unittest import TestCase

import psycopg2
import pytest


from app import create_app
from app.api.version3.exceptions import UserNotFoundError, EmailNotUniqueError
from app.api.version3.models.users import UserModel, UserManager
from app.api.version3.models.users import NORMAL
from app.db_config import create_tables, destroy_tables


class UserModelTests(TestCase):

    def test_initializing_a_user(self):
        user = UserModel("bob", "bob@email.com", "burgers")
        self.assertEqual(user.name, "bob")
        self.assertEqual(user.email, "bob@email.com")
        self.assertEqual(user.role, NORMAL)

    
    def test_user_object_presentation(self):
        user = UserModel("bob", "bob@email.com", "burgers")
        self.assertEqual(repr(user),
                         "User(bob, bob@email.com, %s)" % NORMAL)

    def test_user_in_dictionary_format(self):
        user = UserModel("bob", "bob@email.com", "burgers")
        user_dict = {
            "name": "bob",
            "email": "bob@email.com",
            "role": NORMAL
        }
        self.assertEqual(user.to_dict(), user_dict)


class TestUserManager(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        create_tables()
        self.manager = UserManager()

    def tearDown(self):
        destroy_tables('users')
        self.app_context.pop()

    def test_saving_a_new_user(self):
        user = UserModel("bob", "bob@email.com", "burgers")
        result = self.manager.save(user)
        user.id = 1
        self.assertEqual(result, user)
        
        # test saving a user with a similar email
        user2 = UserModel("bobby", "bob@email.com", "burgers")
        with self.assertRaises(EmailNotUniqueError):
            self.manager.save(user2)

    def test_fetching_user_by_id(self):
        user = UserModel("bob", "bob@email.com", "burgers")
        self.manager.save(user)
        result = self.manager.fetch_by_id(1)
        user.id = 1
        self.assertEqual(result, user)

        # test fetching a user who does not exist
        with self.assertRaises(UserNotFoundError):
            self.manager.fetch_by_id(2)
