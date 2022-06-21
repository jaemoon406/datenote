from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

# from rest_framework.decorators import detail_route, list_route
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from apps.book.models import Book
from .serializers import BookListSerializer, BookSerializer
from rest_framework.decorators import action
from rest_framework import generics
from django.contrib.auth import get_user_model
from apps.util.json_response import *
User = get_user_model()


class Board(ViewSet):
    def get_view_name(self):
        return


class BookCreate(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        BookSerializer.create(self,validated_data=request.data)

        return Response(json_success("S0001", ""), status=status.HTTP_201_CREATED)


class BookViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookListSerializer

    def list(self, request):
        queryset = Book.objects.filter(is_public=False)
        serializer = BookListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, many=True)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # def create(self,request):
