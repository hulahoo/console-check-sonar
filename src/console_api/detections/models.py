"""Models for detections app"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    BigIntegerField,
    DateTimeField,
    DecimalField,
    JSONField,
    Model,
    TextField,
    UUIDField,
)

from console_api.feed.models import Feed, IndicatorFeedRelationship
from console_api.indicator.models import IndicatorTagRelationship
from console_api.tag.models import Tag


class Detection(Model):
    """Event detection"""

    source = TextField(
        "Источник",
    )

    source_message = TextField(
        "Текст входящего сообщения от SIEM",
    )

    source_event = JSONField(
        "Результат парсинга входящего сообщения от SIEM",
    )

    details = JSONField(
        "Дополнительная информация",
    )

    indicator_id = UUIDField(
        "Обнаруженный Индикатор для данного события",
    )

    detection_event = JSONField(
        "Объект с информацией об обнаружении",
    )

    detection_message = TextField(
        "Текст исходящего сообщения во внешнюю ИС (SIEM)",
    )

    tags_weight = DecimalField(
        "Вес тэгов Индикатора на момент обнаружения",
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        decimal_places=5,
        max_digits=8,
    )

    indicator_weight = DecimalField(
        "Вес Индикатора на момент обнаружения",
        decimal_places=5,
        max_digits=8,
    )

    created_at = DateTimeField(
        "Дата создания обнаружения",
        auto_now_add=True,
    )

    def save(self, *args, **kwargs):
        if not self.details:
            self.details = {}

    @property
    def tags_ids(self) -> tuple[int]:
        """Return tags ids linked with the detection"""

        tags = (
            Tag.objects.get(id=relationship.tag_id)
            for relationship in IndicatorTagRelationship.objects.filter(
                indicator_id=self.indicator_id,
            )
        )

        return (
            {
                "id": tag.id,
                "title": tag.title,
                "weight": tag.weight,
            } for tag in tags
        )

    @property
    def feeds_ids(self) -> tuple[int]:
        """Return feeds ids linked with the detection's indicator"""

        return tuple(
            relationship.feed_id
            for relationship in IndicatorFeedRelationship.objects.filter(
                indicator_id=self.indicator_id,
            )
        )

    @property
    def feeds_names(self) -> tuple[str]:
        """Return feeds titles linked with detection's indicator"""

        return tuple(
            Feed.objects.get(id=feed_id).title
            for feed_id in self.feeds_ids
        )

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Обнаружение"
        verbose_name_plural = "Обнаружения"

        ordering = ["-created_at"]
        db_table = "detections"


class DetectionTagRelationship(Model):
    """Custom ManyToMany relationship table for Detection and Tag"""

    detection_id = BigIntegerField("ID обнаружения")

    tag_id = BigIntegerField("ID тега")

    created_at = DateTimeField("Дата создания связи", auto_now_add=True)

    def __str__(self) -> str:
        return f"DetectionTagRelationship ({self.id})"

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Связь M2M «Обнаружение-Тэг»"
        verbose_name_plural = "Связи M2M «Обнаружение-Тэг»"

        ordering = ["-created_at"]
        db_table = "detection_tag_relationships"


class DetectionFeedRelationship(Model):
    """Custom ManyToMany relationship table for Detection and Feed"""

    detection_id = BigIntegerField("ID обнаружения")

    feed_id = BigIntegerField("ID фида")

    created_at = DateTimeField("Дата создания связи", auto_now_add=True)

    def __str__(self) -> str:
        return f"DetectionFeedRelationship ({self.id})"

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Связь M2M «Обнаружение-Фид»"
        verbose_name_plural = "Связи M2M «Обнаружение-Фид»"

        ordering = ["-created_at"]
        db_table = "detection_feed_relationships"
