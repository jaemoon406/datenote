import random

import django.db.utils
from django.core.cache import cache
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model, authenticate
from django.template.context_processors import csrf
from django.conf import settings

from rest_framework import status, generics, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action

from apps.user.models import UserManager
from apps.user.serializers import UserDetailSerializer
from apps.auths.serializers import SignUpSerializer
from apps.core.handler.response_form.error import json_error
from apps.core.handler.response_form.success import json_success
from apps.core.handler.exceptions.error import AlreadyExists

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer: SignUpSerializer):
        try:
            User.objects.create_user(**serializer.validated_data)

        except ValueError as e:
            if str(e.args).rfind('email') > 0:
                return JsonResponse(json_error('E0006'), status=status.HTTP_200_OK)
            elif str(e.args).rfind('username') > 0:
                return JsonResponse(json_error('E0005'), status=status.HTTP_200_OK)
            elif str(e.args).rfind('password') > 0:
                return JsonResponse(json_error('E0004'), status=status.HTTP_200_OK)
            else:
                return JsonResponse(json_error('E0400'), status=status.HTTP_400_BAD_REQUEST)

        except django.db.utils.IntegrityError as e:
            if str(e.args).rfind('email') > 0:
                return JsonResponse(json_error('E0007'), status=status.HTTP_200_OK)
            elif str(e.args).rfind('username') > 0:
                return JsonResponse(json_error('E0008'), status=status.HTTP_200_OK)
            else:
                return JsonResponse(json_error('E0400'), status=status.HTTP_400_BAD_REQUEST)

        except django.db.utils.DataError as e:
            if str(e.args).rfind('too long') > 0:
                return JsonResponse(json_error('E0017'), status=status.HTTP_200_OK)

        except KeyError:
            return JsonResponse(json_error('E0002'), status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def login(self, request):
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
            response = Response()
            data = request.data
            username = data['username']
            password = data['password']
            # user = login(request, username=username, password=password)

            user = authenticate(request, username=username, password=password)
            if not user:
                return Response(json_error("E0005"), status=status.HTTP_200_OK)
            refresh = RefreshToken.for_user(user)

            user_queryset = User.objects.filter(id=user.id)
            user_dic = user_queryset.values()[0]
            serializer = UserDetailSerializer(data=user_dic)
            serializer.is_valid()
            # data = get_tokens_for_user(user)
            # print(csrf(request))
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_KEY'],
                value=refresh.access_token,
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            )

            response.data = json_success("S0008", serializer.data)
            return response
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


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
