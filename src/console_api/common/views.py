from typing import Optional

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from console_api.constants import CREDS_ERROR
from console_api.services import CustomTokenAuthentication


class CommonAPIView(APIView):
    def custom_authenticate(self, request: Request) -> Optional[Response]:
        if not CustomTokenAuthentication().authenticate(request):
            return Response({"detail": CREDS_ERROR}, status=status.HTTP_403_FORBIDDEN)
