from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserManager

class UserControl(APIView):
    def post(self, request):
        data = request.data
        UserManager.create_user(
            self,
            email=data.get('email'),
            username=data.get('username'),
            password=data.get('password')
        )
