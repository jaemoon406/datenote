from django.contrib import admin
from django.urls import path
from apps.user.views import *

urlpatterns = [
    path('signup/', UserControl.as_view(), name='user-control'),
]
