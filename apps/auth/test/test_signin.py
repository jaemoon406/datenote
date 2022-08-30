import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from apps.util.json_response import json_success, json_error

User = get_user_model()


class SignInTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('signin')
        self.content_type = 'application/json'
        self.user = User.objects.create_user(
            username='testtest1',
            email='testuser@test.com',
            password='dlwoans1'
        )

    def test_signin_success(self):
        data = {
            "username": "testtest1",
            "password": "dlwoans1",
        }
        response = self.client.post(self.url, json.dumps(data),  content_type=self.content_type)
        self.assertEqual(response.status_code, 200)

    def test_signin_emtpy_username(self):
        data = {
            "username": "",
            "password": "dlwoans1",
        }
        response = self.client.post(self.url, json.dumps(data),  content_type=self.content_type)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), json_error('E0005'))

    def test_signin_emtpy_password(self):
        data = {
            "username": "testest1",
            "password": "",
        }
        response = self.client.post(self.url, json.dumps(data),  content_type=self.content_type)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), json_error('E0005'))
