"""Models for audit_logs app"""

from django.db.models import (
    BigIntegerField,
    CharField,
    DateTimeField,
    JSONField,
    Model,
)


class AuditLogs(Model):
    """User's actions logs"""

    service_name = CharField(
        "Название сервиса или таблицы",
        max_length=128,
    )

    user_id = BigIntegerField(
        "ID пользователя",
        null=True,
        blank=True,
    )

    user_name = CharField(
        "Имя пользователя",
        max_length=256,
        null=True,
        blank=True,
    )

    event_type = CharField(
        "Тип события",
        max_length=128,
    )

    object_type = CharField(
        "Тип обьекта",
        max_length=128,
    )

    object_name = CharField(
        "Название обьекта",
        max_length=128,
    )

    description = CharField(
        "Описание операции",
        max_length=256,
    )

    prev_value = JSONField(
        "Прошлое значение",
    )

    new_value = JSONField(
        "Новое значение",
    )

    context = JSONField(
        "Дополнительная информация",
    )

    created_at = DateTimeField(
        "Дата и время записи действия",
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        """Metainformation about the model"""

        db_table = "audit_logs"

        verbose_name = "Журнал действий пользователя"
        verbose_name_plural = "Журналы действий пользователя"

        ordering = ["-created_at"]
