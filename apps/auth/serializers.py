from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

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


class SignInSerializer(serializers.ModelSerializer):
    model = User
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def post(self, data):
        user = User.objects.get(username=data['username'])
        user.check_password(data['password'])


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'profile_image', 'email', 'date_joined']
        # fields = '__all__'
# def post(self, data):
#     user = User.objects.get(username=data['username'])
#     user.check_password(data['password'])
