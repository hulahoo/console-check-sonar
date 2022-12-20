"""Models for detections app"""

from django.db import models

from apps.models.abstract import CreationDateTimeField


class Detection(models.Model):
    """Event detection"""

    source_event = models.JSONField(
        "Информация о событии",
        help_text="Информация об объекте из Kafka",
    )

    indicator_id = models.ForeignKey(
        "indicator.Indicator",
        verbose_name="Обнаруженный индикатор для данного события",
        on_delete=models.PROTECT,
    )

    detection_event = models.JSONField(
        "Информация о событии, которая отправляется во внешнюю ИС (SIEM)",
    )

    tags_weight = models.PositiveBigIntegerField(
        "Вес тегов",
    )

    created_at = CreationDateTimeField(
        "Создано",
    )

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Обнаружение"
        verbose_name_plural = "Обнаружения"

        db_table = "detections"
