from django.contrib.auth import get_user_model, authenticate, login

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.user.serializers import UserDetailSerializer
from apps.auth.serializers import UserSerializer

from apps.auth.serializers import SignUpSerializer
from apps.user.models import UserManager

User = get_user_model()


class SignUp(APIView):
    permission_classes = [AllowAny]
    model = User

    def post(self, request):
        data = request.data
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid()
        username = data.get('username')
        # print(self.,'self')
        UserManager.create_user(self, username=username, email=data.get('email'),
                                password=data.get('password'))
        # user = User.objects.filter(username=username).values('id', 'username', 'email', 'nickname', )
        user = User.objects.filter(username=username)
        UserSerializer(data=user)
        return Response({"result": user[0]})


class SignIn(APIView):
    permission_classes = [BasePermission]

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            ######
            refresh = RefreshToken.for_user(user)
            # serializer = UserDetailSerializer(data=user)
            data = {
                'user': user,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response({'result': data})
