"""Views for users app"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from .serializers import AuthTokenSerializer
from console_api.users.models import Token, User
from console_api.services import (
    CustomTokenAuthentication,
    get_hashed_password,
    get_not_fields_error,
)


class UserView(APIView):

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, user_id: int) -> Optional[User]:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Delete user
        """
        user = self.get_object(user_id=kwargs.pop("user_id"))
        if user:
            user.deleted_at = datetime.now()
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={"detail": "User not found"},
        )

    def post(self, request: Request, user_id: int) -> Response:
        """
        Change user data
        """
        user = self.get_object(user_id=user_id)

        if not user:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": "User not found"},
            )

        if error_400 := get_not_fields_error(request, ('role', 'new-pass', 'full-name')):
            return error_400

        if not User.objects.filter(id=user_id).exists():
            return Response(
                {"detail": "User does not exist"},
                status=HTTP_400_BAD_REQUEST,
            )

        new_pass = request.data.get("new-pass")
        new_role = request.data.get("role")
        new_full_name = request.data.get("full-name")

        user.full_name = new_full_name
        user.role = new_role
        user.password = get_hashed_password(new_pass)
        user.save()

        return Response(status=HTTP_200_OK)


class UserDetail(APIView):

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        error_400 = get_not_fields_error(
            request, ('login', 'pass-hash', 'full-name', 'role'),
        )

        if error_400:
            return error_400

        user_login = request.data.get('login')

        if not User.objects.filter(login=user_login).exists():
            User.objects.create(
                login=user_login,
                password=request.data.get('pass-hash'),
                full_name=request.data.get('full-name'),
                role=request.data.get('role'),
            )

        return Response(status=HTTP_201_CREATED)

    def get(self, request: Request, *args, **kwargs) -> Response:
        data = [
            {
                "id": user.id,
                "login": user.login,
                "full-name": user.full_name,
                "role": user.role,
                "created-at": user.created_at,
                "updated-at": user.updated_at,
            }
            for user in User.objects.filter(deleted_at=None)
        ]

        return Response({"results": data}, status=HTTP_200_OK)


class Logout(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs) -> Response:
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class CustomAuthTokenView(ObtainAuthToken):
    """Custom token authorization generator"""

    def post(self, request: Request, *args, **kwargs) -> Response:
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
                token = Token.objects.create(key=user_token, user_id=user.pk)
                token.save()
        except Exception as error:
            return Response(
                {"detail": str(error)},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response({
            'access-token': user_token,
            'user-id': user.pk,
        })


class DeleteAuthToken(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """Delete token"""
        access_token = kwargs.get("access_token")

        if not Token.objects.filter(key=access_token).exists():
            return Response(
                {"detail": "Token doesn't exists"},
                status=HTTP_400_BAD_REQUEST
            )

        Token.objects.get(key=access_token).delete()

        return Response(status=HTTP_200_OK)
