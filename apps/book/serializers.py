from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Book, Board
from apps.user.serializers import UserDetailSerializer

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True, many=True, required=False)  # ManyToMany

    def create(self, **validated_data):
        data = validated_data['validated_data']
        users = data.pop('users')
        book = Book.objects.create(name=data['name'], description=data['description'], is_public=data['is_public'],
                                   password=data['password'])
        for user_id in users:
            book.user.add(user_id['id'])

        return book

    class Meta:
        model = Book
        fields = '__all__'
        # depth = 1


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
