from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.user import views
from apps.user.views import *
import pprint

User = get_user_model()
router = DefaultRouter()

# router.register(r'user', views.UserViewSet, basename='user')
# pprint.pprint(router.urls)

urlpatterns = [
    # path('', include(router.urls)),
    # path('signup/', SignUp.as_view(), name='user-control'),
    # path('signin/', SignIn.as_view()),
]
