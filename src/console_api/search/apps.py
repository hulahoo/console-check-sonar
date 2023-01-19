"""Config for search app"""

from django.apps import AppConfig


class SearchConfig(AppConfig):
    """Config class for search app"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'console_api.search'
