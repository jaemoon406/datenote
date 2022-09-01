import os

from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer

from .serializers import BookListSerializer, BookSerializer, BookRetrieveSerializer
from apps.util.views import query_debugger
from apps.book.models import Book, BookMember
from apps.util.encryption import AESCipher
from apps.util.json_response import *
from apps.util.paginations import ListPagination
from django.shortcuts import get_object_or_404
from apps.util.permissions import BookMemberCheck, BookOwnerCheck

User = get_user_model()
aes = AESCipher(key=os.environ.get('PRIVATE_KEY'))


class BookViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all().order_by('-created')
    serializer_class = BookSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = ListPagination

    def list(self, request, *args, **kwargs):
        self.queryset = Book.objects.filter(is_public=False)
        return super().list(self, request, *args, **kwargs)

    def retrieve(self, request, pk, *args, **kwargs):
        qs = Book.objects.filter(id=pk)
        instance = get_object_or_404(qs)
        serializer = BookRetrieveSerializer(instance)

        if instance.is_public is False:
            if BookMemberCheck.has_permission(instance, request.user):
                return Response(serializer.data)
            else:
                return Response(json_error("E0403"), status=status.HTTP_200_OK)
        serializer = BookRetrieveSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user:
            data = request.data
            data['owner'] = request.user
            BookSerializer.create(self, validated_data=data)
            return Response(json_success('S0001', {"Success"}), status=status.HTTP_201_CREATED)
        else:
            return Response(json_error('E0403'), status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if BookOwnerCheck.has_permission(instance, request.user):
            return super().destroy(self, request, *args, **kwargs)
        else:
            return Response(json_error('E0403'), status=status.HTTP_200_OK)


