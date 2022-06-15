from django.urls import path, include
from .views import *


urlpatterns = [
    path('apiroot/', APIRootView.as_view(), name='api-root'),
]
