"""Models for detections app"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from console_api.apps.feed.models import Feed
from console_api.apps.models.abstract import CreationDateTimeField
from console_api.apps.indicator.models import Indicator
from console_api.apps.tag.models import IndicatorTagRelationship
from console_api.apps.feed.models import IndicatorFeedRelationship


class Detection(models.Model):
    """Event detection"""

    source_message = models.TextField()

    source_event = models.JSONField(
        "Информация о событии",
        help_text="Информация о Событии (Объект из Kafka)",
    )

    indicator_id = models.UUIDField()

    detection_event = models.JSONField(
        "Информация о событии, которая отправляется во внешнюю ИС (SIEM)",
    )

    detection_message = models.TextField()

    tags_weight = models.DecimalField(
        "Вес тегов",
        validators=[MaxValueValidator(100), MinValueValidator(1)],
        decimal_places=5,
        max_digits=20,
    )

    indicator_weight = models.DecimalField(
        decimal_places=5,
        max_digits=20,
    )

    created_at = CreationDateTimeField(
        "Создано",
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
    def feeds_ids(self) -> str | None:
        """Return feed's ids linked with the detection"""

        return [
            rel.feed_id
            for rel in DetectionFeedRelationship.objects.filter(
                detection_id=self.id,
            )
        ]

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Обнаружение"
        verbose_name_plural = "Обнаружения"

        db_table = "detections"


class DetectionTagRelationship(models.Model):
    """Custom ManyToMany relationship table for Detection and Tag"""

    detection_id = models.BigIntegerField()

    tag_id = models.BigIntegerField()

    created_at = CreationDateTimeField(
        "Дата и время создания связи",
    )

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Связь обнаружение-тег"
        verbose_name_plural = "Связи обнаружение-тег"

        db_table = "detection_tag_relationships"


class DetectionFeedRelationship(models.Model):
    """Custom ManyToMany relationship table for Detection and Feed"""

    detection_id = models.BigIntegerField()

    feed_id = models.BigIntegerField()

    created_at = CreationDateTimeField(
        "Дата и время создания связи",
    )

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Связь обнаружение-фид"
        verbose_name_plural = "Связи обнаружение-фид"

        db_table = "detection_feed_relationships"
