import django.db.utils
from django.contrib.auth import get_user_model, authenticate, login
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import action


from apps.util.json_response import json_success, json_error
from apps.auth.serializers import SignUpSerializer
from apps.user.serializers import UserDetailSerializer
from apps.user.models import UserManager

User = get_user_model()


class SignUp(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny]
    model = User

    def post(self, request):
        try:
            data = request.data
            serializer = SignUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            username = data.get('username')
            UserManager.create_user(self, username=username, email=data.get('email'),
                                    password=data.get('password'))

            return JsonResponse(json_success('S0009', None), status=status.HTTP_201_CREATED)

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
            username = data.get('username')
            password = data.get('password')
            # user = login(request, username=username, password=password)
            user = authenticate(request, username=username, password=password)
            print(user)
            refresh = RefreshToken.for_user(user)

            user_queryset = User.objects.filter(username=username)
            print(user,type(user))
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
