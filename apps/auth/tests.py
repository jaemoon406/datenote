import unittest
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

User = get_user_model()


class TestSignUp(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_success(self):
        c = Client()
        signup_data = {
            "username": "testtest1",
            "password": "testtest1",
            "email": "test1@test.test"
        }
        response = c.post(path='v1/account/signup/', data=signup_data, HTTP_ACCEPT='application/json', )
        self.assertEqual('')