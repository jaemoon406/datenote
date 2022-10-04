from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction, DatabaseError
from django.db.utils import DataError
from rest_framework.exceptions import ValidationError


from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Book, Board, BookMember
from apps.user.serializers import UserDetailSerializer

User = get_user_model()


class BookListSerializer(serializers.ModelSerializer):
    member = UserDetailSerializer(read_only=True, many=True)  # ManyToMany

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'is_public', 'member', 'created', 'modified']


class BoardRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id',)


# class BookMemberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BookMember
#         fields = '__all__'

#
# class BookOwnerSerializer(serializers.ModelSerializer):
#     bookmember = BookMemberSerializer(BookMember.objects.filter(owner=True))
#
#     class Meta:
#         model = User
#         fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    member = UserDetailSerializer(many=True, required=False)

    @transaction.atomic
    def create(self, validated_data):
        try:
            with transaction.atomic():
                owner = validated_data.pop('owner')
                book = Book.objects.create(**validated_data)
                BookMember.objects.create(book_id=book.id, user_id=owner.id, owner=1)

        except DataError:
            raise ValidationError
        return book


    class Meta:
        model = Book
        fields = ['id', 'name', 'is_public', 'member', 'created', 'modified']


class BookRetrieveSerializer(serializers.ModelSerializer):
    member = UserDetailSerializer(many=True, required=False)

    class Meta:
        model = Book
        fields = ['id', 'name', 'is_public', 'description', 'member', 'created', 'modified']


# ModelSerializer의 속도 저하로 인한 Serializer 사용
class BoardSerializer(serializers.Serializer):
    user = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='User'
    )
    book = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='Book'
    )
    description = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=50)
    date = serializers.DateTimeField()
    locate = serializers.CharField(max_length=50)
