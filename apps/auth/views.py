import random

import django.db.utils
from django.core.cache import cache
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model, authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.decorators import api_view, permission_classes

from apps.user.models import UserManager
from apps.user.serializers import UserDetailSerializer
from apps.core.handler.response_form.error import json_error
from apps.core.handler.response_form.success import json_success


User = get_user_model()


class SignUp(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny]
    model = User

    def post(self, request):
        try:
            data = request.data
            username = data.get('username')
            UserManager.create_user(self, username=username, email=data.get('email'),
                                    password=data.get('password'))
            return JsonResponse(json_success('S0009', None), status=status.HTTP_201_CREATED)

        except ValueError as e:
            if str(e.args).rfind('email') > 0:
                return JsonResponse(json_error('E0006'), status=status.HTTP_400_BAD_REQUEST)
            elif str(e.args).rfind('username') > 0:
                return JsonResponse(json_error('E0005'), status=status.HTTP_400_BAD_REQUEST)
            elif str(e.args).rfind('password') > 0:
                return JsonResponse(json_error('E0004'), status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(json_error('E0400'), status=status.HTTP_400_BAD_REQUEST)

        except django.db.utils.IntegrityError as e:
            if str(e.args).rfind('email') > 0:
                return JsonResponse(json_error('E0007'), status=status.HTTP_400_BAD_REQUEST)
            elif str(e.args).rfind('username') > 0:
                return JsonResponse(json_error('E0008'), status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse(json_error('E0400'), status=status.HTTP_400_BAD_REQUEST)

        except django.db.utils.DataError as e:
            if str(e.args).rfind('too long') > 0:
                return JsonResponse(json_error('E0017'), status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return JsonResponse(json_error('E0002'), status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    permission_classes = [BasePermission]

    def post(self, request):
        try:
            data = request.data
            username = data['username']
            password = data['password']
            # user = login(request, username=username, password=password)
            user = authenticate(request, username=username, password=password)
            refresh = RefreshToken.for_user(user)

            user_queryset = User.objects.filter(username=username)
            user_dic = user_queryset.values()[0]
            serializer = UserDetailSerializer(data=user_dic)
            serializer.is_valid()
            token = {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
            return Response(json_success("S0008", {'user': serializer.data, 'token': token}), status=status.HTTP_200_OK)
        except AttributeError:
            return Response(json_error("E0005"), status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response(json_error("E0005"), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def issue_auth_code(request):
    data = request.data
    phone = data['phone_num']
    r = list()
    for i in range(6):
        r.append(random.randrange(0, 9))
    number = ''.join(map(str, r))
    cache.set(str(phone), number, timeout=180)
    """
    Email이나 Phone으로 인증 받아야 함
    """
    return Response(json_success("S0001", "Create"), status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def check_auth_code(request):
    data = request.data
    phone = data['phone_num']
    code = data['auth_code']
    if cache.get(phone) == code:
        return Response(json_success("S0004", ["OK"]), status=status.HTTP_200_OK)
    else:
        return Response(json_error("E0003"), status=status.HTTP_200_OK)
