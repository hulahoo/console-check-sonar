from django.db import models

from console_api.apps.models.abstract import CreationDateTimeField


class AuditLogs(models.Model):
    service_name = models.CharField(
        "Название сервиса или таблицы",
        max_length=128
    )
    user_id = models.BigIntegerField("ID пользователя")
    event_type = models.CharField(
        "Тип события",
        max_length=128
    )
    object_type = models.CharField(
        "Тип обьекта",
        max_length=128
    )
    object_name = models.CharField(
        "Информация об обьекте",
        max_length=128
    )
    description = models.CharField(
        "Описание операции",
        max_length=256
    )
    prev_value = models.JSONField("Прошлое значение")
    new_value = models.JSONField("Новое значение")
    context = models.JSONField()
    created_at = CreationDateTimeField("создано")
