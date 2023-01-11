"""Serializers for users app"""

from hashlib import sha256

from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (
    ValidationError,
    CharField,
    Serializer,
    ModelSerializer,
)
from rest_framework.validators import UniqueValidator

from console_api.users.models import User


class UserSerializer(ModelSerializer):
    """Serializer for User model"""

    class Meta:
        """Metainformation about the serializer"""

        model = User
        exclude = []


class RegisterSerializer(ModelSerializer):
    """Serializer for user registration"""

    login = CharField(
        max_length=255,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    pass_hash = CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    class Meta:
        """Metainformation about the serializer"""

        model = User
        fields = ("login", "pass_hash")
        extra_kwargs = {"id": {"read_only": True}, "pass-hash": {"source": "pass_hash"}}

    def create(self, validated_data):
        user = User.objects.create(
            login=validated_data["login"],
        )
        user.set_password(validated_data["pass_hash"])
        user.save()

        return user


class AuthTokenSerializer(Serializer):
    """Serializer for auth token generation"""

    login = CharField()
    password = CharField()

    def validate(self, attrs: dict) -> dict:
        """Validate user"""

        login = attrs.get("login")
        password = attrs.get("password")

        if login and password:
            hashed_password = sha256(bytes(password.encode()))

            if User.objects.filter(login=login).exists():
                user = User.objects.get(login=login)

                if hashed_password.hexdigest() != user.password:
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
