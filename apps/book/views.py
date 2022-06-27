from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

# from rest_framework.decorators import detail_route, list_route
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.renderers import JSONRenderer
from rest_framework.pagination import PageNumberPagination

from .serializers import BookListSerializer, BookSerializer
from apps.book.models import Book
from apps.util.json_response import *

User = get_user_model()


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
        queryset = Book.objects.filter(is_public=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, many=True)
        serializer = self.get_serializer(instance)
        return serializer.data

    def create(self, request, *args, **kwargs):
        request.data['owner'] = request.user
        BookSerializer.create(self, validated_data=request.data)
        return Response(json_success("S0001", ""), status=status.HTTP_201_CREATED)
