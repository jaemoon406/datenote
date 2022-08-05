import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from apps.util.json_response import json_success, json_error

User = get_user_model()


class SignUpTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    #
    # def tearDown(self):
    #     User.objects.all().delete()

    def test_signup_success(self):
        url = reverse('signup')
        data = {
            "username": "testtest1",
            "password": "dlwoans1",
            "email": "test1@test.test"
        }
        response = self.client.post(url, json.dumps(data), 'json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.json(), json_success('S009', None))
