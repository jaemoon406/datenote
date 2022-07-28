import os

from apps.util.encryption import AESCipher
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.renderers import JSONRenderer
from rest_framework.pagination import PageNumberPagination

from apps.util.views import query_debugger
from .serializers import BookListSerializer, BookSerializer
from apps.book.models import Book, BookMember
from apps.util.json_response import *

User = get_user_model()
aes = AESCipher(key=os.environ.get('PRIVATE_KEY'))


class ListPagination(PageNumberPagination):
    page_size = 5


class Board(ViewSet):
    def get_view_name(self):
        return


class BookViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = ListPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk, *args, **kwargs):
        instance = self.get_object()
        serializer = BookListSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user:
            data = request.data
            data['owner'] = request.user
            data['password'] = aes.encrypt(data['password'])
            BookSerializer.create(self, validated_data=data)
            return Response(json_success('S0001', {"Success"}), status=status.HTTP_201_CREATED)
        else:
            return Response(json_error('E0403'), status=status.HTTP_200_OK)
