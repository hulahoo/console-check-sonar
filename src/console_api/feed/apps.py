"""Config for feed app"""

from django.apps import AppConfig


class FeedConfig(AppConfig):
    """Config class for feed app"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'console_api.feed'
