"""Models for indicator app"""

from uuid import uuid4

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from console_api.feed.models import IndicatorFeedRelationship, Feed
from console_api.tag.models import IndicatorTagRelationship


RELATE_TO = "users.User"


class Indicator(models.Model):
    """Indicator"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    ioc_type = models.CharField(
        "Тип индикатора",
        max_length=32,
    )

    value = models.CharField(
        "Значение индикатора",
        max_length=1024,
    )

    context = models.JSONField(
        "Данные контекста из Фидов и из Сервисов Обогащения Информацией",
    )

    is_sending_to_detections = models.BooleanField(
        "Обнаружение по индикатору должно улетать в detections?",
        default=True,
    )

    is_false_positive = models.BooleanField(
        "Ложноположительный индикатор?",
        default=False,
    )

    weight = models.DecimalField(
        "Вес индикатора",
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        decimal_places=3,
        max_digits=6,
    )

    feeds_weight = models.DecimalField(
        "Вес фида",
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        decimal_places=3,
        max_digits=6,
    )

    time_weight = models.DecimalField(
        "Вес времени индикатора",
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        decimal_places=3,
        max_digits=6,
    )

    tags_weight = models.DecimalField(
        "Средний вес тегов фида",
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        decimal_places=3,
        max_digits=6,
    )

    is_archived = models.BooleanField(
        "Статус архивирования",
        default=False,
    )

    false_detected_counter = models.BigIntegerField(
        "Количество ложных срабатываний",
    )

    positive_detected_counter = models.BigIntegerField(
        "Количество подтвержденных срабатываний",
    )

    total_detected_counter = models.BigIntegerField(
        "Всего срабатываний",
    )

    first_detected_at = models.DateTimeField(
        "Дата и время первого срабатывания",
    )

    last_detected_at = models.DateTimeField(
        "Дата и время последнего срабатывания",
    )

    created_by = models.BigIntegerField(
        "Указывается, когда Индикатор создан пользователем",
    )

    external_source_link = models.CharField(
        max_length=255,
    )

    created_at = models.DateTimeField(
        "Дата и время создания",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Дата и время обновления",
        auto_now=True,
    )

    @property
    def feeds(self) -> tuple:
        """Return tuple of feeds that linked with the indicator"""

        feeds_ids = [
            relationship.feed_id
            for relationship in IndicatorFeedRelationship.objects.filter(
                indicator_id=self.id,
            )
        ]

        return (
            {"id": feed_id, "name": Feed.objects.get(id=feed_id).title}
            for feed_id in feeds_ids
        )

    @property
    def activities(self) -> tuple:
        """Return tuple of activities that linked with the indicator"""

        return (
            {
                "type": activity.activity_type,
                "details": activity.details,
                "created-at": activity.created_at,
            }
            for activity in IndicatorActivities.objects.filter(
                indicator_id=self.id,
            )
        )

    @property
    def feeds_names(self) -> tuple:
        """Return tuple of names for feeds that linked with the indicator"""

        feeds = [
            relationship.feed_id
            for relationship in IndicatorFeedRelationship.objects.filter(
                indicator_id=self.id,
            )
        ]

        return (Feed.objects.get(id=feed_id).title for feed_id in feeds)

    @property
    def tags_ids(self) -> tuple:
        """Return tuple of tags ids that linked with the indicator"""

        return (
            relationship.tag_id
            for relationship in IndicatorTagRelationship.objects.filter(
                indicator_id=self.id,
            )
        )

    def __str__(self) -> str:
        return f"{self.value} ({self.ioc_type})"

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Индикатор"
        verbose_name_plural = "Индикаторы"

        db_table = "indicators"

        unique_together = ("ioc_type", "value")


class IndicatorActivities(models.Model):
    """Timeline of activity for each Indicator"""

    indicator_id = models.UUIDField(default=uuid4, editable=False)

    activity_type = models.CharField("Тип", max_length=32)

    details = models.JSONField()

    created_at = models.DateTimeField(
        "Дата и время создания",
        auto_now_add=True,
    )

    created_by = models.BigIntegerField(null=True)

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Таймлайн активности по индикатору"
        verbose_name_plural = "Таймлайны активностей по индикаторам"

        db_table = "indicator_activities"


class Session(models.Model):
    """User session"""

    user_id = models.BigIntegerField("Ссылка на users.id")

    access_token = models.CharField(
        "Токен доступа MD5",
        max_length=255,
    )

    last_activity_at = models.DateTimeField(
        "Дата и время последней активности",
        editable=False,
    )

    created_at = models.DateTimeField(
        "Дата и время создания",
        auto_now_add=True,
    )

    def save(self, *args, **kwargs) -> None:
        self.last_activity_at = timezone.now()

        super().save(*args, **kwargs)

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Сессия"
        verbose_name_plural = "Сессии"

        db_table = "sessions"