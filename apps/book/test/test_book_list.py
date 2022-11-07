from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from apps.book.models import Book

User = get_user_model()


class BookListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('signin')
        self.content_type = 'application/json'
        self.user = User.objects.create_user(
            username='testtest1',
            email='testuser@test.com',
            password='dlwoans1'
        )
        for i in range(15):
            self.book = Book.objects.create(name='abc'+i, description='desc'+i, member=1)

    def test_book_list_success(self):
        response = self.client.get(path=self.url, content_type=self.content_type)
        print(response.content_params,'par')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.)
