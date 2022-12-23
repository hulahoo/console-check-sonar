"""Models for detections app"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from console_api.apps.feed.models import Feed
from console_api.apps.models.abstract import CreationDateTimeField


class Detection(models.Model):
    """Event detection"""

    source_event = models.JSONField(
        "Информация о событии",
        help_text="Информация о Событии (Объект из Kafka)",
    )

    indicator = models.ForeignKey(
        "indicator.Indicator",
        verbose_name="Обнаруженный индикатор для данного события",
        on_delete=models.PROTECT,
    )

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

    tags = models.ManyToManyField(
        "tag.Tag",
        blank=True,
        null=True,
        through="DetectionTagRelationship",
    )

    # переписать все проперти в сервисах
    @property
    def context(self) -> str:
        return self.indicator.context

    @property
    def feed_name(self) -> str:
        if Feed.objects.filter(
            indicators__id__contains=self.indicator.id
        ).exists():
            return Feed.objects.filter(
                indicators__id__contains=self.indicator.id
            )[0].title

    @property
    def ioc_id(self):
        return self.indicator.id

    @property
    def provider(self):
        feed_provider = None

        if Feed.objects.filter(
            indicators__id__contains=self.indicator.id
        ).exists():
            feed_provider = Feed.objects.filter(
                indicators__id__contains=self.indicator.id
            )[0].provider

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

    detection = models.ForeignKey(
        "detections.Detection",
        on_delete=models.CASCADE,
    )

    tag = models.ForeignKey(
        "tag.Tag",
        on_delete=models.CASCADE,
    )

    created_at = CreationDateTimeField(
        "Дата и время создания связи",
    )

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Связь обнаружение-тег"
        verbose_name_plural = "Связи обнаружение-тег"

        db_table = "detection_tag_relationships"
