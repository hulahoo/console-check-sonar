"""Config for audit_logs app"""

from django.apps import AppConfig


class AuditLogsConfig(AppConfig):
    """Config class"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'audit_logs'
