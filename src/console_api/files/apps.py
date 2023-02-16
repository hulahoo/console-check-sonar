"""Config for files app"""

from django.apps import AppConfig


class FilesConfig(AppConfig):
    """Config class for files app"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'console_api.files'
