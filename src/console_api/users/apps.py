"""Config for users app"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Config class for users app"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'console_api.users'
