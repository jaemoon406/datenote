from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction, DatabaseError

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Book, Board, BookMember
from apps.user.serializers import UserDetailSerializer
from django.shortcuts import get_object_or_404

User = get_user_model()


class BookListSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True, many=True, allow_empty=False)  # ManyToMany
    member = UserDetailSerializer(read_only=True, many=True)  # ManyToMany

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'is_public', 'member', 'created', 'modified']


class BoardRetrieveSerializer(serializers.ModelSerializer):
    # user = serializers.  # ManyToOne
    # comment = serializers.  # OneToMany

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id',)


class BookMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMember
        fields = '__all__'


class BookOwnerSerializer(serializers.ModelSerializer):
    bookmember = BookMemberSerializer(BookMember.objects.filter(owner=True))

    class Meta:
        model = User
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    member = UserDetailSerializer(many=True, required=False)

    @transaction.atomic
    def create(self, validated_data):
        with transaction.atomic():
            owner = validated_data.pop('owner')
            password = validated_data['password']



            validated_data['password'] = '4567'
            book = Book.objects.create(**validated_data)
            BookMember.objects.create(book_id=book.id, user_id=owner.id, owner=1)

        return book

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'is_public', 'member', 'created', 'modified']
        # fields = '__all__'
