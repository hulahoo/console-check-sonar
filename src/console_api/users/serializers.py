"""Serializers for users app"""

from rest_framework.serializers import (
    ValidationError,
    CharField,
    Serializer,
)

from console_api.users.models import User
from console_api.services import get_hashed_password


class AuthTokenSerializer(Serializer):
    """Serializer for auth token generation"""

    login = CharField()
    password = CharField()

    def validate(self, attrs: dict) -> dict:
        """Validate user"""

        login = attrs.get("login")
        password = attrs.get("password")

        if login and password:
            hashed_password = get_hashed_password(password)

            if User.objects.filter(login=login).exists():
                user = User.objects.get(login=login)

                if hashed_password != user.password:
                    raise ValidationError(
                        "Unable to log in with provided credentials.",
                        code="authorization",
                    )

                if not user.is_active:
                    raise ValidationError(
                        "User account is disabled.",
                        code="authorization",
                    )
            else:
                raise ValidationError(
                    "Unable to log in with provided credentials.",
                    code="authorization",
                )
        else:
            raise ValidationError(
                'Must include "login" and "password".',
                code="authorization",
            )

        attrs["user"] = user

        return attrs
