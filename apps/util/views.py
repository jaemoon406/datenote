from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, BasePermission


class APIRootView(APIView):
    permission_classes = [BasePermission]

    def get(self, request):
        # year = now().year
        data = {
            '회원가입': reverse('signup'),
            '로그인': reverse('signin'),
            '토큰 재발급': reverse('token_refresh'),
            '토큰 확인': reverse('token_refresh'),
            '토큰 블랙리스트': reverse('token_blacklist'),
            '': reverse(''),
            '': reverse(''),
            '': reverse(''),
        }
        return Response(data)
