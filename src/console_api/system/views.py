"""System views"""

from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.status import HTTP_200_OK
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from console_api.config.logger_config import logger


@api_view(('GET',))
@require_http_methods(["GET"])
@renderer_classes((JSONRenderer,))
def readiness_and_liveness_view(request) -> Response:
    """Выдаёт статус о полной готовности сервиса (readiness + liveness)"""

    return Response(status=HTTP_200_OK)


@api_view(('GET',))
@require_http_methods(["GET"])
@renderer_classes((JSONRenderer,))
def readiness_view(request) -> Response:
    """Выдаёт статус о готовности сервиса принимать входящий трафик"""

    logger.info("Readiness checking started")

    return Response(status=HTTP_200_OK)


@api_view(('GET',))
@require_http_methods(["GET"])
@renderer_classes((JSONRenderer,))
def liveness_view(request) -> Response:
    """Выдаёт статус о работоспособности сервиса"""

    logger.info("Liveness checking started")

    return Response(status=HTTP_200_OK)


@api_view(('GET',))
@require_http_methods(["GET"])
@renderer_classes((JSONRenderer,))
def metrics_view(request) -> Response:
    """Выдаёт метрики сервиса"""

    metrics = generate_latest().replace(b'"', b'').replace(b'\n', b'<br>')

    return Response(data=metrics, content_type=CONTENT_TYPE_LATEST)


@api_view(('GET',))
@require_http_methods(["GET"])
@renderer_classes((JSONRenderer,))
def api_res(request) -> Response:
    data = {
        "openapi:": "3.0.0",
        "info": {
            "title": "Событийный шлюз",
            "version": "0.3",
        },
        "paths": {}
        }
    return Response(data=data)
