"""Views for users app"""

from uuid import uuid4

from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)


from .serializers import AuthTokenSerializer
from console_api.services import CustomTokenAuthentication
from console_api.users.models import Token, User
from console_api.constants import CREDENTIALS_ERROR


@api_view(["POST", "GET"])
def users_view(request: Request) -> Response:
    """Create a new user or return list of users"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response(
            {"detail": CREDENTIALS_ERROR},
            status=HTTP_403_FORBIDDEN
        )

    if request.method == "POST":
        user_login = request.data.get('login')

        if not User.objects.filter(login=user_login).exists():
            User.objects.create(
                login=request.data.get('login'),
                password=request.data.get('pass-hash'),
                full_name=request.data.get('full-name'),
                role=request.data.get('role'),
            )

        return Response(status=HTTP_201_CREATED)

    elif request.method == "GET":
        data = [
            {
                "id": user.id,
                "login": user.login,
                "full-name": user.full_name,
                "role": user.role,
                "created-at": user.created_at,
                "updated-at": user.updated_at,
            }
            for user in User.objects.all()
        ]

        return Response({"results": data}, status=HTTP_200_OK)

    return Response(status=HTTP_400_BAD_REQUEST)


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
