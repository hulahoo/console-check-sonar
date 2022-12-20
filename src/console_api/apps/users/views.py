from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

<<<<<<< HEAD:src/console_api/apps/users/views.py
from .serializers import RegisterSerializer, UserSerializer
from .models import User
=======
from console_api.api.users.serializers import RegisterSerializer, UserSerializer
from console_api.apps.users.models import User
>>>>>>> main:src/console_api/api/users/views.py


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
