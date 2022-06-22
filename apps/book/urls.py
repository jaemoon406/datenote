from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.reverse import reverse
from .views import BookViewSet


router = DefaultRouter()
router.register(r'books', BookViewSet, basename='booklist')

urlpatterns = [
    path('', include(router.urls)),
    # path('post/', BookCreate.as_view(), name='book-create'),
]
