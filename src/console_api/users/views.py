"""Views for users app"""

from uuid import uuid4

from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST


from .serializers import RegisterSerializer, AuthTokenSerializer
from console_api.services import CustomTokenAuthentication
from console_api.users.models import Token


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = RegisterSerializer
    authentication_classes = [CustomTokenAuthentication]


class Logout(APIView):
    authentication_classes = [CustomTokenAuthentication]
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

            if Token.objects.filter(user_id=user.pk).exists():
                user_token = Token.objects.get(user_id=user.pk).key
            else:
                user_token = uuid4()
                t = Token.objects.create(key=user_token, user_id=user.pk)
                t.save()
        except Exception as e:
            return Response(
                {
                    'errors': [
                        {
                            key: value[0]
                            for key, value in e.detail.items()
                        }
                    ]
                },
                status=HTTP_400_BAD_REQUEST,
            )

        return Response({
            'access-token': user_token,
            'user-id': user.pk,
        })
