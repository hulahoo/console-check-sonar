from django.db import models


class PlatformSettings(models.Model):
    """PlatformSettings - data source"""

    id = models.BigAutoField(
        primary_key=True,
    )

    key = models.CharField(
        "Название сервиса",
        max_length=128
    )

    value = models.JSONField(
        "Значение"
    )

    created_at = models.DateTimeField(
        "Дата и время создания",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Дата и время обновления",
        auto_now_add=True,
    )

    created_by = models.BigIntegerField(
        "ID пользователя"
    )

    class Meta:
        """Meta information about the model"""

        db_table = "platform_settings"
