from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.user import views
from apps.auths.views import *
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView)

User = get_user_model()
router = DefaultRouter()

# router.register(r'user', views.UserViewSet, basename='user')
# pprint.pprint(router.urls)

urlpatterns = [
    # path('', include(router.urls)),
    path('signup/', SignUp.as_view(), name='signup'),
    path('signin/', SignIn.as_view(), name='signin'),
    # path('signin/', TokenObtainPairView.as_view(), name='signin'),
    path('token/obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('issue_code/', issue_auth_code, name='create_authentication_code'),
    path('check_code/', check_auth_code, name='check_authentication_code'),
]
