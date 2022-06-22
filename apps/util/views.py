from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated


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
