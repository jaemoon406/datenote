from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Book, Board, BookMember
from apps.user.serializers import UserDetailSerializer
from django.shortcuts import get_object_or_404

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True, many=True, required=False)  # ManyToMany
    owner = UserDetailSerializer(read_only=True, many=True, required=False)  # ManyToMany

    def get_view_name(self):
        return

    def create(self, validated_data):
        users = validated_data.pop('users')
        book = Book.objects.create(**validated_data)
        for user_id in users:
            BookMember.objects.create(book_id=book.id, user_id=user_id['id'])
        return book


    class Meta:
        model = Book
        fields = '__all__'
        depth = 1


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
        read_only_fields = ('id',)
