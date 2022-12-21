from rest_framework.decorators import api_view
from rest_framework.response import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from config.log_conf import logger


@api_view(["GET"])
def readiness(request):
    """
    Текущее состояние готовности сервиса
    """
    logger.info("Readiness checking started")
    return Response({"status": "UP"})


@api_view(["GET"])
def liveness(request):
    """
    Возвращает информацию о работоспособности сервиса
    """
    logger.info("Liveness checking started")
    return Response({"status": "UP"})

@api_view(["GET"])
def metrics(request):
    """
    Возвращает метрики сервиса
    """
    return Response(data=generate_latest(), content_type=CONTENT_TYPE_LATEST)


@api_view(["GET"])
def api_routes(request):
    return Response({
        "openapi:": "3.0.0",
        "info": {
            "title": "Консоль мониторинга и управления",
            "version": "0.0.1",
        },
        "paths": {
            "/api/doc/": {
                "get": {
                    "description": "Документация SWAGGER",
                    "responses": {
                        "200": {
                            "description": "Успешный вход",
                        }
                    }
                }
            },
            "/console/sessions/": {
                "post": {
                    "description": "Создать Новую Сессию для Пользователя",
                    "responses": {
                        "200": {
                            "description": "ОК",
                        }
                    }
                }
            },
            "/console/logout/": {
                "get": {
                    "description": "Логаут(Удалить Сессию Пользователя)",
                    "responses": {
                        "200": {
                            "description": "ОК",
                        }
                    }
                }
            },
            "/console/statistics/feeds/": {
                "get": {
                    "description": "Получить Статистику По Фидам",
                    "responses": {
                        "200": {
                            "description": "ОК",
                        }
                    }
                }
            },
            "/console/statistics/indicators/": {
                "get": {
                    "description": "Получить Статистику По Индикаторам",
                    "responses": {
                        "200": {
                            "description": "ОК",
                        }
                    }
                }
            },
            "/console/statistics/matched-indicators/": {
                "get": {
                    "description": "Получить Статистику По Обнаруженным Индикаторам",
                    "responses": {
                        "200": {
                            "description": "ОК",
                        }
                    }
                }
            },
            "/console/statistics/matched-objects/": {
                "get": {
                    "description": "Получить Статистику По Обнаруженным Объектам",
                    "responses": {
                        "200": {
                            "description": "ОК",
                        }
                    }
                }
            },
            "/console/statistics/checked-objects/": {
                "get": {
                    "description": "ОК",
                    "responses": {
                        "200": {
                            "description": "",
                        }
                    }
                }
            },
            "/console/statistics/feeds-intersections/": {
                "get": {
                    "description": "Получить Статистику По Пересечениям",
                    "responses": {
                        "200": {
                            "description": "ОК",
                        }
                    }
                }
            },
        }
    })

