import time
import functools
from django.db import connection, reset_queries

from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated

def query_debugger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        reset_queries()
        number_of_start_queries = len(connection.queries)
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        end    = time.perf_counter()
        number_of_end_queries = len(connection.queries)
        print("-------------------------------------------------------------------")
        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {number_of_end_queries-number_of_start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        print("-------------------------------------------------------------------")
        return result
    return wrapper

class APIRootView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        user = self.request.user
        print(user)
        # print(request.headers)
        # year = now().year
        path = '127.0.0.1:8000'
        data = {
            'update': '2022-06-15T19:25:22.705883',
            '======':'==========================',
            '회원가입': path + reverse('signup'),
            '로그인': path + reverse('signin'),
            '토큰 재발급': path + reverse('token_refresh'),
            '토큰 확인': path + reverse('token_refresh'),
            '토큰 블랙리스트': path + reverse('token_blacklist'),
            # '': reverse(''),
            # '': reverse(''),
        }
        return Response(data)
