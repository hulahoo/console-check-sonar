"""Models for platform_settings app"""

from django.db.models import (
    BigAutoField,
    BigIntegerField,
    CharField,
    DateTimeField,
    Model,
    JSONField,
)


class PlatformSettings(Model):
    """PlatformSettings - data source"""

    id = BigAutoField(
        primary_key=True,
    )

    key = CharField(
        "Название сервиса",
        max_length=128
    )

    value = JSONField(
        "Значение"
    )

    created_at = DateTimeField(
        "Дата и время создания",
        auto_now_add=True,
    )

    updated_at = DateTimeField(
        "Дата и время обновления",
        auto_now_add=True,
    )

    created_by = BigIntegerField(
        "ID пользователя"
    )

    class Meta:
        """Meta information about the model"""

        db_table = "platform_settings"
