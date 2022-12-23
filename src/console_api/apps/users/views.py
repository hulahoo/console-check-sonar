from rest_framework import generics, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import (
    RegisterSerializer, UserSerializer, AuthTokenSerializer,
)
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = RegisterSerializer


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class CustomAuthTokenView(ObtainAuthToken):
    """Custom token authorization generator"""

    def post(self, request, *args, **kwargs):
        try:
            serializer = AuthTokenSerializer(
                data=request.data,
                context={'request': request},
            )

            serializer.is_valid(raise_exception=True)

            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
        except Exception as e:
            return Response({
                'errors': [{"detail": str(e)}]
            })

        return Response({
            'access-token': token.key,
            'user-id': user.pk,
        })
