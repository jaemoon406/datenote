from django.contrib import admin
from django.urls import path, include
from .views import BookCreate


urlpatterns = [
    path('post/', BookCreate.as_view(), name='book-create'),
]
