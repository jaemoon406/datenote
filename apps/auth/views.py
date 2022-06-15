from django.contrib.auth import get_user_model, authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.serializers import UserDetailSerializer
from apps.auth.serializers import SignUpSerializer
from apps.user.models import UserManager
from rest_framework.reverse import reverse

User = get_user_model()


class SignUp(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        UserManager.create_user(self)
        serializer.is_valid()
        serializer.save()


class SignIn(APIView):
    permission_classes = [BasePermission]

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            ######
            refresh = RefreshToken.for_user(user)
            # serializer = UserDetailSerializer(data=user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response({'result': data})


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
