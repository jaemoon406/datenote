import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from apps.util.json_response import json_success, json_error

User = get_user_model()


class SignInTestCase(APITestCase):
    def setUp(self):
        self.user = self.setup_user()
        self.client = APIClient()
        self.url = reverse('signin')

    @staticmethod
    def setup_user():
        return User.objects.create_user(
            username='testtest1',
            email='testuser@test.com',
            password='dlwoans1'
        )

    def test_signin_success(self):
        data = {
            "username": "testtest1",
            "password": "dlwoans1",
        }
        response = self.client.post(self.url, json.dumps(data), 'json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_success('S0008', None))

    def test_signin_emtpy_username(self):
        data = {
            "username": "",
            "password": "dlwoans1",
        }
        response = self.client.post(self.url, json.dumps(data), 'json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), json_error('E0005'))

    def test_signin_emtpy_password(self):
        data = {
            "username": "testest1",
            "password": "",
        }
        response = self.client.post(self.url, json.dumps(data), 'json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), json_error('E0005'))