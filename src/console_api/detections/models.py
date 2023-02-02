"""Models for detections app"""
from typing import List

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from console_api.feed.models import Feed, IndicatorFeedRelationship


CREATED_AT = "Дата и время создания"


class DetectionTagRelationship(models.Model):
    """Custom ManyToMany relationship table for Detection and Tag"""

    detection_id = models.BigIntegerField()

    tag_id = models.BigIntegerField()

    created_at = models.DateTimeField(
        CREATED_AT,
        auto_now_add=True,
    )

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Связь обнаружение-тег"
        verbose_name_plural = "Связи обнаружение-тег"

        db_table = "detection_tag_relationships"


class Detection(models.Model):
    """Event detection"""

    source = models.TextField(
        "Источник",
    )

    source_message = models.TextField(
        "Текст входящего сообщения от SIEM",
    )

    source_event = models.JSONField(
        "Результат парсинга входящего сообщения от SIEM",
    )

    details = models.JSONField(
        "Дополнительная информация",
    )

    indicator_id = models.UUIDField(
        "Обнаруженный Индикатор для данного события",
    )

    detection_event = models.JSONField(
        "Объект с информацией об обнаружении",
    )

    detection_message = models.TextField(
        "Текст исходящего сообщения во внешнюю ИС (SIEM)",
    )

    tags_weight = models.DecimalField(
        "Вес тэгов Индикатора на момент обнаружения",
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        decimal_places=5,
        max_digits=8,
    )

    indicator_weight = models.DecimalField(
        "Вес Индикатора на момент обнаружения",
        decimal_places=5,
        max_digits=8,
    )

    created_at = models.DateTimeField(
        "Дата создания обнаружения",
        auto_now_add=True,
    )

    @property
    def tags_ids(self) -> tuple:
        """Return tuple of tags ids that linked with the detection"""

        return (
            relationship.tag_id for relationship in
            DetectionTagRelationship.objects.filter(
                detection_id=self.id,
            )
        )

    @property
    def feeds_ids(self) -> List[str] | None:
        """Return feed's ids linked with the detection"""

        return [
            rel.feed_id
            for rel in DetectionFeedRelationship.objects.filter(
                detection_id=self.id,
            )
        ]

    @property
    def feeds_names(self) -> tuple:
        """Return tuple of feeds that linked with detection's indicator"""

        feeds_ids = [
            relationship.feed_id for relationship in
            IndicatorFeedRelationship.objects.filter(
                indicator_id=self.indicator_id,
            )
        ]

        return (
            Feed.objects.get(id=feed_id).title
            for feed_id in feeds_ids
        )

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Обнаружение"
        verbose_name_plural = "Обнаружения"
        ordering = ["-created_at"]
        db_table = "detections"


class DetectionFeedRelationship(models.Model):
    """Custom ManyToMany relationship table for Detection and Feed"""

    detection_id = models.BigIntegerField()

    feed_id = models.BigIntegerField()

    created_at = models.DateTimeField(
        CREATED_AT,
        auto_now_add=True,
    )

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Связь обнаружение-фид"
        verbose_name_plural = "Связи обнаружение-фид"

        db_table = "detection_feed_relationships"
