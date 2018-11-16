# test_user_datastore.py

import unittest

from app.api.version2.models import UserDataStore


class UserDataStoreTests(unittest.TestCase):

    def setUp(self):
        self.store = UserDataStore()

    def tearDown(self):
        self.store.db.clear()
 
    def test_adding_user_to_store(self):
        self.store.db.clear()
        payload = self.store.save('bob', 'bob@email.com', 'burgers')
        self.assertEqual(payload, {'id': 1,
                                   'name': 'bob',
                                   'email': 'bob@email.com',
                                   'login_status': 'logged out'})
        # test user emails are unique
        payload2 = self.store.save('bobby', 'bob@email.com', 'robert')
        self.assertEqual(payload2, {
            "error": "Email address already in use"
        })

    def test_authenticating_a_user(self):
        self.store.save('bob', 'bob@gmail.com', 'burgers')
        self.assertTrue(self.store.authenticate("bob@gmail.com", "burgers"))
        self.assertFalse(self.store.authenticate("bob@gmail.com", "banana"))
        self.assertFalse(self.store.authenticate("bob", "burgers"))

    def test_fetching_a_user_by_id(self):
        self.store.save('bob', 'bob@email.com', 'burgers')
        payload = self.store.fetch_by_id(1)
        expected_json = {
            "id": 1,
            "name": "bob",
            "email": "bob@email.com"
        }
        self.assertEqual(payload, expected_json)

    def test_logging_in_a_user(self):
        self.store.save('bob', 'bob@gmail.com', 'burgers')
        payload = self.store.login_user('bob@gmail.com', 'burgers')
        expected_json =  {
            "id": 1,
            "name": "bob",
            "email": "bob@gmail.com",
            "login_status": "logged in"
        }
        self.assertEqual(payload, expected_json)

        # login with wrong credentials
        payload2 = self.store.login_user("bob", "burgers")
        payload3 = self.store.login_user("bob@gmail.com", "burgerking")
        payload4 = self.store.login_user("linda", "lindapassword")
        expected_json = {
            "error": "Invalid Credentials"
        }
        self.assertEqual(payload2, expected_json)
        self.assertEqual(payload3, expected_json)
        self.assertEqual(payload4, expected_json)
