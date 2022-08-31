from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.pagination import PageNumberPagination



class Success(APIException):
    status_code = status.HTTP_200_OK
    default_detail = _('ok')
    default_code = 'ok'


class ListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):

        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        try:
            self.page = paginator.page(page_number)
        except Exception as exc:
            msg = {
                'totalCount': len(queryset),
                'countPerPage': page_size,  # offset
                'currentPage': page_number,  # 현재 페이지
                'results': [],
            }
            raise Success(msg)

        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        self.request = request
        return list(self.page)