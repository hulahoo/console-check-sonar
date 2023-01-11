"""Config for statistics app"""

from django.apps import AppConfig


class StatisticsConfig(AppConfig):
    """Config class for statistics app"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'console_api.statistics'
