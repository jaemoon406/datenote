from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.book.models import BookMember

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'profile_image', 'last_login', 'email', 'date_joined']


class BookMemberSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = BookMember
        fields = ['owner', 'user']
