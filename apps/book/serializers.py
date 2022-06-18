from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Board

User = get_user_model()


class BookListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, many=True, allow_empty=False)  # ManyToMany

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'is_public', 'user', 'created', 'modified']


class BoardRetrieveSerializer(serializers.ModelSerializer):
    # user = serializers.  # ManyToOne
    # comment = serializers.  # OneToMany

    class Meta:
        model = Board
        fields = '__all__'
