from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    nickname = serializers.CharField(required=False)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            nickname=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    model = User
    fields = ['id', 'username', 'nickname', 'profile_image', 'last_active', 'email', 'date_joined']
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def post(self, data):
        user = User.objects.get(username=data['username'])
        user.check_password(data['password'])
