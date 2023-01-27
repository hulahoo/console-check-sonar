"""Views for platform-settings app"""
import json

from datetime import datetime

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND
)

from console_api.platform_settings.models import PlatformSettings
from console_api.platform_settings.serializers import PlatformSettingsSerializer
from console_api.services import CustomTokenAuthentication


class PlatformSettingsView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, key: str) -> Response:
        settings = PlatformSettings.objects.filter(key=key)

        if not settings:
            return Response({"detail": f"unknown service {key}"}, status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_200_OK, data=settings[0].value)

    def post(self, request: Request, key: str) -> Response:
        platform_settings = PlatformSettings.objects.filter(key=key)

        if platform_settings:
            settings = platform_settings[0]
            settings.value = json.loads(request.body)
            settings.updated_at = datetime.now()
        else:
            user, _ = CustomTokenAuthentication().authenticate(request)

            settings = PlatformSettings(
                value=json.loads(request.body),
                key=key,
                created_by=user.id
            )

        settings.save()

        return Response(status=HTTP_200_OK)
