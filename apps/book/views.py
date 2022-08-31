import os

from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.renderers import JSONRenderer

from .serializers import BookListSerializer, BookSerializer
from apps.util.views import query_debugger
from apps.book.models import Book, BookMember
from apps.util.encryption import AESCipher
from apps.util.json_response import *
from apps.util.paginations import ListPagination


User = get_user_model()
aes = AESCipher(key=os.environ.get('PRIVATE_KEY'))

class BookViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    queryset = Book.objects.all().order_by('-created')
    serializer_class = BookSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = ListPagination

    def list(self, request, *args, **kwargs):
        self.queryset = Book.objects.filter(is_public=False)
        return super().list(self, request, *args, **kwargs)

    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(self, request, pk, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if request.user:
            data = request.data
            data['owner'] = request.user
            data['password'] = aes.encrypt(data['password'])
            request = request
            BookSerializer.create(self, validated_data=data)
            return super().create(self, request, *args, **kwargs)
            # return Response(json_success('S0001', {"Success"}), status=status.HTTP_201_CREATED)
        else:
            return Response(json_error('E0403'), status=status.HTTP_200_OK)
