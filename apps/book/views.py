from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.book.models import Book


class Board(ViewSet):
    def get_view_name(self):
        return


# class BoardRetrieve(AP):
#     def get

class BookCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        Book.objects.create(
            name=data.get('name'),
            description=data.get('description'),
            is_public=data.get('is_public'),
            password=data.get('password')
        )
        return Response({}, status=status.HTTP_201_CREATED)
