from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = []


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=255,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(source="pass")

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('pass')

        if login and password:
            user = authenticate(username=login, password=password)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(
                        msg, code='authorization',
                    )
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user

        return attrs
