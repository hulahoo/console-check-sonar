"""Views for users app"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from django.db.models import Q
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
    HTTP_404_NOT_FOUND,
)

from .serializers import AuthTokenSerializer, UserUpdateSerializer
from console_api.users.models import Token, User
from console_api.services import (
    CustomTokenAuthentication,
    create_audit_log_entry,
    get_hashed_password,
    get_not_fields_error,
)
from console_api.users.constants import LOG_SERVICE_NAME


class UserChangePasswordView(APIView):
    """View for changing user's password"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, user_id: int) -> Optional[User]:
        try:
            return User.objects.get(deleted_at=None, id=user_id)
        except User.DoesNotExist:
            return None

    def post(self, request: Request, user_id: int) -> Response:
        """Change user password"""

        user = self.get_object(user_id=user_id)

        if not user:
            return Response(
                data={"detail": "User not found"},
                status=HTTP_404_NOT_FOUND,
            )

        if error_400 := get_not_fields_error(request, ("password",)):
            return error_400

        if not User.objects.filter(id=user_id).exists():
            return Response(
                {"detail": "User does not exist"},
                status=HTTP_400_BAD_REQUEST,
            )

        prev_user_value = {
            "login": user.login,
            "full_name": user.full_name,
            "updated_at": str(user.updated_at)
            if user.updated_at
            else user.updated_at,
        }

        new_password = request.data.get("password")

        user.password = get_hashed_password(new_password)
        user.save()

        create_audit_log_entry(
            request,
            {
                "table": LOG_SERVICE_NAME,
                "event_type": "change-user-password",
                "object_type": "user",
                "object_name": "User",
                "description": "Change user password",
                "prev_value": prev_user_value,
                "new_value": {
                    "login": user.login,
                    "full_name": user.full_name,
                    "updated_at": str(user.updated_at)
                    if user.updated_at
                    else user.updated_at,
                },
            },
        )

        return Response(status=HTTP_200_OK)


class UserView(APIView):

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, user_id: int) -> Optional[User]:
        try:
            return User.objects.get(deleted_at=None, id=user_id)
        except User.DoesNotExist:
            return None

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """Delete user"""

        if user := self.get_object(user_id=kwargs.pop("user_id")):
            prev_user_value = {
                "login": user.login,
                "full_name": user.full_name,
                "deleted_at": str(user.deleted_at)
                if user.deleted_at
                else user.deleted_at,
            }

            user.deleted_at = datetime.now()

            if Token.objects.filter(user=user.id).exists():
                Token.objects.get(user=user.id).delete()

            user.save()

            create_audit_log_entry(
                request,
                {
                    "table": LOG_SERVICE_NAME,
                    "event_type": "delete-user",
                    "object_type": "user",
                    "object_name": "User",
                    "description": "Delete a user",
                    "prev_value": prev_user_value,
                    "new_value": {
                        "login": user.login,
                        "full_name": user.full_name,
                        "deleted_at": str(user.deleted_at)
                        if user.deleted_at
                        else user.deleted_at,
                    },
                },
            )

            return Response(status=status.HTTP_200_OK)

        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={"detail": "User not found"},
        )

    def post(self, request: Request, user_id: int) -> Response:
        """Change user data"""

        if not User.objects.filter(id=user_id).exists():
            return Response(
                {"detail": f"User with id {user_id} doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(id=user_id)

        prev_user_value = {
            "login": user.login,
            "full_name": user.full_name,
            "updated_at": str(user.updated_at)
            if user.updated_at
            else user.updated_at,
        }

        serializer = UserUpdateSerializer(
            user,
            data=request.data,
            partial=True,
            fields=request.data.keys()
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if new_password := request.data.get("password"):
            user.password = get_hashed_password(new_password)
            user.save()

        serializer.save()

        create_audit_log_entry(
            request,
            {
                "table": LOG_SERVICE_NAME,
                "event_type": "update-user",
                "object_type": "user",
                "object_name": "User",
                "description": "Update user data",
                "prev_value": prev_user_value,
                "new_value": {
                    "login": user.login,
                    "full_name": user.full_name,
                    "updated_at": str(user.updated_at)
                    if user.updated_at
                    else user.updated_at,
                },
            },
        )

        return Response(status=HTTP_200_OK)


class UserDetail(APIView):

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        error_400 = get_not_fields_error(
            request,
            ("login", "password", "full-name", "role"),
        )

        if error_400:
            return error_400

        user_login = request.data.get("login")

        if User.objects.filter(~Q(deleted_at=None), login=user_login).exists():
            user = User.objects.get(login=user_login)
            user.deleted_at = None
            user.save()
        elif not User.objects.filter(login=user_login).exists():
            full_name = request.data.get("full-name")
            role = request.data.get("role")

            pass_hash = get_hashed_password(request.data.get("password"))

            User.objects.create(
                login=user_login,
                password=pass_hash,
                full_name=full_name,
                role=role,
            )

            create_audit_log_entry(
                request,
                {
                    "table": LOG_SERVICE_NAME,
                    "event_type": "create-user",
                    "object_type": "user",
                    "object_name": "User",
                    "description": "Create a user",
                    "new_value": {
                        "login": user_login,
                        "full_name": full_name,
                        "role": role,
                    },
                },
            )
        elif User.objects.filter(login=user_login).exists():
            return Response(
                {"detail": f"User {user_login} already exists"},
                status=HTTP_400_BAD_REQUEST,
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


class CustomAuthTokenView(ObtainAuthToken):
    """Custom token authorization generator"""

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            serializer = AuthTokenSerializer(
                data=request.data,
                context={"request": request},
            )

            serializer.is_valid(raise_exception=True)

            user = serializer.validated_data["user"]

            if not User.objects.filter(login=user.login, deleted_at=None).exists():
                return Response(
                    {"detail": "User does not exist"},
                    status=HTTP_400_BAD_REQUEST,
                )

            if Token.objects.filter(user_id=user.pk).exists():
                user_token = Token.objects.get(user_id=user.pk).key
            else:
                user_token = uuid4()
                token = Token.objects.create(key=user_token, user_id=user.pk)
                token.save()

                create_audit_log_entry(
                    request,
                    {
                        "table": "Console API | token",
                        "event_type": "create-token",
                        "object_type": "token",
                        "object_name": "Token",
                        "description": "Create token with id",
                        "new_value": {
                            "key": str(token.key),
                            "created_at":
                                str(token.created_at)
                                if token.created_at else token.created_at,
                        },
                    },
                )
        except Exception as error:
            return Response(
                {"detail": str(error)},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "access-token": user_token,
                "user-id": user.pk,
                "user-role": user.role,
            }
        )


class DeleteAuthTokenView(APIView):
    """Delete an authentication token"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """Delete token"""

        access_token = kwargs.get("access_token")

        if not Token.objects.filter(key=access_token).exists():
            return Response(
                {"detail": "Token doesn't exists"}, status=HTTP_400_BAD_REQUEST
            )

        token = Token.objects.get(key=access_token)
        prev_token_value = {
            "key": str(token.key),
            "created_at":
                str(token.created_at)
                if token.created_at else token.created_at,
        }

        token.delete()

        create_audit_log_entry(
            request,
            {
                "table": "Console API | token",
                "event_type": "delete-token",
                "object_type": "token",
                "object_name": "Token",
                "description": "Delete the token",
                "prev_value": prev_token_value,
            },
        )

        return Response(status=HTTP_200_OK)
