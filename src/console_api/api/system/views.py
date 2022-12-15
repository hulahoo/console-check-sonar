from rest_framework.decorators import api_view
from rest_framework.response import Response
from config.log_conf import logger


@api_view(["GET"])
def readiness():
    """
    Текущее состояние готовности сервиса
    """
    logger.info("Readiness checking started")
    return Response({"status": "UP"})


@api_view(["GET"])
def liveness():
    """
    Возвращает информацию о работоспособности сервиса
    """
    logger.info("Liveness checking started")
    return Response({"status": "UP"})


@api_view(["GET"])
def api_routes():
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
            "/api/sessions/": {
                "post": {
                    "description": "Создать Новую Сессию для Пользователя",
                    "responses": {
                        "200": {
                            "description": "ОК",
                        }
                    }
                }
            },
            "/api/logout/": {
                "get": {
                    "description": "Логаут(Удалить Сессию Пользователя)",
                    "responses": {
                        "200": {
                            "description": "ОК",
                        }
                    }
                }
            },
            "/api/statistics/feeds/": {
                "get": {
                    "description": "Получить Статистику По Фидам",
                    "responses": {
                        "200": {
                            "description": "ОК",
                        }
                    }
                }
            },
            "/api/statistics/indicators/": {
                "get": {
                    "description": "Получить Статистику По Индикаторам",
                    "responses": {
                        "200": {
                            "description": "ОК",
                        }
                    }
                }
            },
            "/api/statistics/matched-indicators/": {
                "get": {
                    "description": "Получить Статистику По Обнаруженным Индикаторам",
                    "responses": {
                        "200": {
                            "description": "ОК",
                        }
                    }
                }
            },
            "/api/statistics/matched-objects/": {
                "get": {
                    "description": "Получить Статистику По Обнаруженным Объектам",
                    "responses": {
                        "200": {
                            "description": "ОК",
                        }
                    }
                }
            },
            "/api/statistics/checked-objects/": {
                "get": {
                    "description": "ОК",
                    "responses": {
                        "200": {
                            "description": "",
                        }
                    }
                }
            },
            "/api/statistics/feeds-intersections/": {
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
