"""Config for indicator app"""

from django.apps import AppConfig


class IndicatorConfig(AppConfig):
    """Config class for indicator app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "console_api.indicator"
