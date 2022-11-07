import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from apps.core.handler.response_form.success import json_success


class IssueAuthorizationCodeTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create_authentication_code')
        self.content_type = 'application/json'
    def test_issue_code_success(self):
        data = {'phone_num': "01047696070"}
        response = self.client.post(self.url, json.dumps(data), content_type=self.content_type)
        self.assertEqual(response.json(), json_success("S0001", "Create"))
        self.assertEqual(response.status_code, 201)

