from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def readiness():
    """
    Возвращает информацию о готовности сервиса
    """
    return Response({"description": "Текущее состояние готовности сервиса"})


@api_view(["GET"])
def liveness():
    """
    Возвращает информацию о работоспособности сервиса
    """
    return Response({"description": "Возвращает информацию о работоспособности сервиса"})
