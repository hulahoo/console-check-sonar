"""Models for indicator app"""

from uuid import uuid4

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from apps.models.abstract import BaseModel, CreationDateTimeField


INDICATOR_TYPES = (
    ("ip", "ip"),
    ("domain", "domain"),
    ("hash", "hash"),
)

ACTIVITIES_TYPE = (
    ("add_comment", "add-comment"),
    ("add_tag", "add-tag"),
    ("remove_tag", "remove-tag"),
    ("move_to_archive", "move-to-archive"),
    ("move_from_archive", "move-from-archive"),
)


class Indicator(BaseModel):
    """Indicator"""

    # Используется CharField, а не UUIDField потому что иначе
    # не получается сделать ManyToMany связь с Feed моделью
    id = models.CharField(
        primary_key=True,
        default=uuid4,
        editable=False,
        max_length=36,
    )

    ioc_type = models.CharField(
        "Тип индикатора",
        max_length=32,
        choices=INDICATOR_TYPES,
    )

    value = models.CharField(
        "Значение индикатора",
        max_length=512,
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

    created_by = models.ForeignKey(
        "users.User",
        help_text="Указывается, когда Индикатор создан пользователем",
        on_delete=models.PROTECT,
        verbose_name="Кем создано",
        null=True,
        blank=True,
    )

    @property
    def feeds_list(self):
        return list(self.feed_set.all())

    @property
    def tags(self):
        return list(self.tag_set.all())

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

    indicator = models.ForeignKey(
        "indicator.Indicator",
        on_delete=models.CASCADE,
        verbose_name="Активность по индикатору",
        related_name="activities",
    )

    type = models.TextField(
        "Тип",
        choices=ACTIVITIES_TYPE,
    )

    details = models.JSONField()

    created_at = CreationDateTimeField(
        "Создано",
    )

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        verbose_name="Кем создано",
    )

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Таймлайн активности по индикатору"
        verbose_name_plural = "Таймлайны активностей по индикаторам"

        db_table = "indicator_activities"


class Session(models.Model):
    """User session"""

    user_id = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        verbose_name="ID пользователя",
    )

    access_token = models.TextField(
        "Токен доступа MD5",
        max_length=255,
    )

    last_activity_at = models.DateTimeField(
        "Дата и время последней активности",
        editable=False,
    )

    created_at = models.DateTimeField(
        "Дата и время создания сессии",
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
