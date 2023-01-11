"""Config for detections app"""

from django.apps import AppConfig


class DetectionsConfig(AppConfig):
    """Config class"""

    default_auto_field = 'django.db.models.BigAutoField'

    name = 'console_api.detections'
