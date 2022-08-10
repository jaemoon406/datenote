import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from apps.util.json_response import json_success, json_error


class IssueAuthorizationCodeTestCase(APITestCase):
    def SetUp(self):
        self.client = APIClient()
        self.url = reverse('create_authentication_code')

    def test_issue_code_success(self):
        data = {'phone_num': '01047696070'}
        response = self.client.post(self.url, json.dumps(data), 'json')
        self.assertEqual(response.json(), json_success("S0001", ["Create"]))
        self.assertEqual(response.status_code, 201)
