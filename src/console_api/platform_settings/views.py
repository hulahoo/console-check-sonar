"""Views for platform-settings app"""
import json

from datetime import datetime

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from console_api.platform_settings.models import PlatformSettings
from console_api.services import (
    CustomTokenAuthentication,
    create_audit_log_entry,
)


class PlatformSettingsView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, key: str) -> Response:
        settings = PlatformSettings.objects.filter(key=key)

        if not settings:
            return Response(
                {"detail": f"unknown service {key}"},
                status=HTTP_404_NOT_FOUND,
            )

        return Response(status=HTTP_200_OK, data=settings[0].value)

    def post(self, request: Request, key: str) -> Response:
        if platform_settings := PlatformSettings.objects.filter(key=key):
            settings = platform_settings[0]

            prev_setting_value = {
                "id": settings.id,
                "key": settings.key,
                "value": settings.value,
                "created_at":
                    str(settings.created_at)
                    if settings.created_at else settings.created_at,
                "updated_at":
                    str(settings.updated_at)
                    if settings.updated_at else settings.updated_at,
                "created_by": settings.created_by,
            }

            settings.value = json.loads(request.body)
            settings.updated_at = datetime.now()

            settings.save()

            create_audit_log_entry(request, {
                "table": "Console API | platform_settings",
                "event_type": "update-platform-settings",
                "object_type": "platform-settings",
                "object_name": "Platform settings",
                "description": f"Update platform settings with key {key}",
                "prev_value": prev_setting_value,
                "new_value": {
                    "id": settings.id,
                    "key": settings.key,
                    "value": settings.value,
                    "created_at":
                        str(settings.created_at)
                        if settings.created_at else settings.created_at,
                    "updated_at":
                        str(settings.updated_at)
                        if settings.updated_at else settings.updated_at,
                    "created_by": settings.created_by,
                },
            })
        else:
            user, _ = CustomTokenAuthentication().authenticate(request)

            settings = PlatformSettings(
                value=json.loads(request.body), key=key, created_by=user.id,
            )

            settings.save()

            create_audit_log_entry(request, {
                "table": "Console API | platform_settings",
                "event_type": "create-platform-settings",
                "object_type": "platform-settings",
                "object_name": "Platform settings",
                "description": f"Create platform settings with key {key}",
                "new_value": {
                    "id": settings.id,
                    "key": settings.key,
                    "value": settings.value,
                    "created_at":
                        str(settings.created_at)
                        if settings.created_at else settings.created_at,
                    "updated_at":
                        str(settings.updated_at)
                        if settings.updated_at else settings.updated_at,
                    "created_by": settings.created_by,
                },
            })

        return Response(status=HTTP_200_OK)
