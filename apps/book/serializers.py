from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Book, Board
from apps.user.serializers import UserDetailSerializer

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookListSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True, many=True, allow_empty=False)  # ManyToMany
    user = UserDetailSerializer(read_only=True, many=True)  # ManyToMany
    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'is_public', 'user', 'created', 'modified']


class BoardRetrieveSerializer(serializers.ModelSerializer):
    # user = serializers.  # ManyToOne
    # comment = serializers.  # OneToMany

    class Meta:
        model = Board
        fields = '__all__'
