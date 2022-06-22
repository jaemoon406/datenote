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

from .serializers import BookListSerializer, BookSerializer
from apps.book.models import Book
from apps.util.json_response import *

User = get_user_model()


class Board(ViewSet):
    def get_view_name(self):
        return

class BookViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        BookSerializer.create(self, request=request.data)
        return Response(json_success("S0001", ""), status=status.HTTP_201_CREATED)







