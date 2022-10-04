from django.contrib.auth import get_user_model, authenticate, login

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend

from apps.book.models import BookMember, Book
from .serializers import BookMemberSerializer
from apps.util.paginations import ListPagination

User = get_user_model()


# class BookMemberViewSet(mixins.CreateModelMixin,
#                         # mixins.RetrieveModelMixin,
#                         mixins.UpdateModelMixin,
#                         mixins.DestroyModelMixin,
#                         mixins.ListModelMixin,
#                         GenericViewSet):
#         serializer_class = BookMemberSerializer
#         permission_classes = [IsAuthenticated]
#         queryset = Book.objects.all()
#         pagination_class = ListPagination
class BookMemberManager(APIView):
    serializer_class = BookMemberSerializer
    permission_classes = [IsAuthenticated]
    queryset = BookMember.objects.all()
    pagination_class = ListPagination
    renderer_classes = [JSONRenderer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username']

    def get(self, request, *args, **kwargs):
        qs = self.queryset.filter(book_id=kwargs['pk'])
        serializer = self.serializer_class(qs,many=True)
        print(serializer.data)
        # Book.objects.filter(id=kwargs['pk'])
        # queryset = self.filter_queryset(self.get_queryset())
        # print(self.get_queryset())
        print(qs)
        return Response(serializer.data)




















