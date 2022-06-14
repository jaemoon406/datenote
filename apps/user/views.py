from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.user.serializers import SignUpSerializer, UserSerializer


# class UserControl(APIView):
#     def post(self, request):
#         data = request.data
#         UserManager.create_user(
#             self,
#             email=data.get('email'),
#             username=data.get('username'),
#             password=data.get('password')
#         )
#
class SignUp(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()


class SignIn(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
