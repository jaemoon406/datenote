import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from apps.util.json_response import json_success, json_error

User = get_user_model()


class SignUpTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('signup')
        self.content_type = 'application/json'

    def test_signup_success(self):
        data = {
            "username": "testtest1",
            "password": "dlwoans1",
            "email": "test1@test.test"
        }
        response = self.client.post(self.url, json.dumps(data), content_type=self.content_type)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.json(), json_success('S0009', None))

    def test_signup_drop_username_error(self):
        data = {
            "username": "",
            "password": "dlwoans1",
            "email": "test1@test.test"
        }
        response = self.client.post(self.url, json.dumps(data), content_type=self.content_type)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.json(), json_error('E0005'))

    def test_signup_drop_password_error(self):
        data = {
            "username": "testtest1",
            "password": "",
            "email": "test1@test.test"
        }
        response = self.client.post(self.url, json.dumps(data), content_type=self.content_type)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.json(), json_error('E0004'))

    def test_signup_drop_email_error(self):
        data = {
            "username": "testtest1",
            "password": "dlwoans1",
            "email": ""
        }
        response = self.client.post(self.url, json.dumps(data), content_type=self.content_type)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.json(), json_error('E0006'))
