"""Views for users app"""

from uuid import uuid4, UUID

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
from django.views.decorators.http import require_POST, require_http_methods, require_GET


from .serializers import AuthTokenSerializer
from console_api.services import CustomTokenAuthentication
from console_api.users.models import Token, User
from console_api.constants import CREDENTIALS_ERROR
from console_api.services import get_hashed_password


@api_view(["POST"])
@require_POST
def change_user_password_view(request: Request, user_id: UUID) -> Response:
    """Change user password"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response(
            {"detail": CREDENTIALS_ERROR},
            status=HTTP_403_FORBIDDEN
        )

    if request.method == "POST":
        for field in 'prev-pass', 'new-pass':
            if not request.data.get(field):
                return Response(
                    {"detail": f"{field} not specified"},
                    status=HTTP_400_BAD_REQUEST,
                )

        if not User.objects.filter(id=user_id).exists():
            return Response(
                {"detail": "User does not exist"},
                status=HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(id=user_id)

        prev_pass = request.data.get("prev-pass")
        new_pass = request.data.get("new-pass")

        if get_hashed_password(prev_pass) != user.password:
            return Response(
                {"detail": "Password is invalid"},
                status=HTTP_400_BAD_REQUEST,
            )

        user.password = get_hashed_password(new_pass)
        user.save()

        return Response(status=HTTP_200_OK)


@api_view(["POST", "GET"])
@require_GET
@require_POST
def users_view(request: Request) -> Response:
    """Create a new user or return list of users"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response(
            {"detail": CREDENTIALS_ERROR},
            status=HTTP_403_FORBIDDEN
        )

    if request.method == "POST":
        for field in 'login', 'pass-hash', 'full-name', 'role':
            if not request.data.get(field):
                return Response(
                    {"detail": f"{field} not specified"},
                    status=HTTP_400_BAD_REQUEST,
                )

        user_login = request.data.get('login')

        if not User.objects.filter(login=user_login).exists():
            User.objects.create(
                login=user_login,
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


@api_view(["DELETE"])
@require_http_methods(["DELETE"])
def delete_auth_token_view(request: Request, access_token: UUID) -> Response:
    """Delete token"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response(
            {"detail": CREDENTIALS_ERROR},
            status=HTTP_403_FORBIDDEN
        )

    if request.method == "DELETE":
        if not Token.objects.filter(key=access_token).exists():
            return Response(
                {"detail": "Token doesn't exists"},
                status=HTTP_400_BAD_REQUEST
            )

        Token.objects.get(key=access_token).delete()

        return Response(status=HTTP_200_OK)
