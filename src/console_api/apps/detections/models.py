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

    source_event = models.JSONField(
        "Информация о событии",
        help_text="Информация о Событии (Объект из Kafka)",
    )

    indicator_id = models.UUIDField()

    detection_event = models.JSONField(
        "Информация о событии, которая отправляется во внешнюю ИС (SIEM)",
    )

    tags_weight = models.BigIntegerField(
        "Вес тегов",
        validators=[MaxValueValidator(100), MinValueValidator(1)],
    )

    created_at = CreationDateTimeField(
        "Создано",
    )

    @property
    def context(self) -> str:
        """Return context for the indicator"""

        if Indicator.objects.filter(id=self.indicator_id).exists():
            return Indicator.objects.get(id=self.indicator_id).context

        return "{}"

    @property
    def tags_ids(self) -> tuple:
        """Return tuple of tags ids that linked with the detection"""

        return (
            relationship.tag_id for relationship in
            IndicatorTagRelationship.objects.filter(
                indicator_id=self.indicator_id,
            )
        )

    @property
    def feed_name(self) -> str | None:
        """Return feed's name linked with the detection"""

        if IndicatorFeedRelationship.objects.filter(
            indicator_id=self.indicator_id
        ).exists():
            relationship = IndicatorFeedRelationship.objects.get(
                indicator_id=self.indicator_id
            )
            feed = Feed.objects.get(id=relationship.feed_id)

            return feed.title

        return None

    @property
    def provider(self) -> str | None:
        """Return detection's provider from it's feed"""

        feed_provider = None

        if IndicatorFeedRelationship.objects.filter(
            indicator_id=self.indicator_id
        ).exists():
            relationship = IndicatorFeedRelationship.objects.get(
                indicator_id=self.indicator_id
            )
            feed_provider = Feed.objects.get(id=relationship.feed_id).provider

        return feed_provider

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
