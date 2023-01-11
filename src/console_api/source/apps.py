"""Config for source app"""

from django.apps import AppConfig


class SourceConfig(AppConfig):
    """Config class for source app"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'console_api.source'
