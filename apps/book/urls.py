from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, main

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='booklist')

urlpatterns = [
    path('', include(router.urls)),
    path('main', main, name='main_page')
]
