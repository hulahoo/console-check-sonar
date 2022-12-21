from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid as uuid

from apps.tag.models import Tag
from apps.common.enums import TypesEnum
from apps.models.abstract import BaseModel


class Indicator(BaseModel):
    """
    Модель индикатора.
    """
    uuid = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(
        "Тип индикатора", max_length=13, default=TypesEnum.IP.value
    )
    category = models.CharField(
        "Категория индикатора", max_length=128, blank=True, null=True
    )
    value = models.CharField("Значение индикатора", max_length=256)
    weight = models.IntegerField(
        "Вес", validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    tag = models.ManyToManyField(Tag, blank=True, null=True)
    false_detected = models.IntegerField(
        "счетчик ложных срабатываний", validators=[MinValueValidator(0)], default=0
    )
    positive_detected = models.IntegerField(
        "счетчик позитивных срабатываний", validators=[MinValueValidator(0)], default=0
    )
    detected = models.IntegerField(
        "общий счетчик срабатываний", validators=[MinValueValidator(0)], default=0
    )
    first_detected_date = models.DateTimeField(
        "Дата первого срабатывания", blank=True, null=True
    )
    last_detected_date = models.DateTimeField(
        "Дата последнего срабатывания", blank=True, null=True
    )
    # Данные об источнике
    supplier_name = models.CharField("Название источника", max_length=128)
    supplier_vendor_name = models.CharField("Название поставщика ", max_length=128)
    supplier_type = models.CharField("Тип поставщика", max_length=64)
    supplier_confidence = models.IntegerField(
        "Достоверность", validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    supplier_created_date = models.DateTimeField(
        "Дата последнего обновления", blank=True, null=True
    )

    context = models.JSONField(
        "Данные контекста из Фидов и из Сервисов Обогащения Информацией",
    )

    # время жизни
    ttl = models.DateTimeField("Дата удаления", blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = "Индикатор"
        verbose_name_plural = "Индикаторы"
        db_table = "indicators"


class IndicatorActivities(BaseModel):
    """
    Модель Активность по Индикатору
    """
    ACTIVITIES_TYPE = (
        ("add_comment", "add-comment"),
        ("add_tag", "add-tag"),
        ("remove_tag", "remove-tag"),
        ("move_to_archive", "move-to-archive"),
        ("move_from_archive", "move-from-archive"),
    )
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, verbose_name='Активность по индикатору',
                                  related_name='activities')
    type = models.CharField(max_length=50, choices=ACTIVITIES_TYPE, verbose_name='Тип')
    details = models.JSONField()

    class Meta:
        verbose_name = "Активность по Индикатору"
        verbose_name_plural = "Активности по Индикатору"
        db_table = "activities"


class Session(models.Model):
    """Пользовательская сессия"""

    user_id = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        verbose_name="ID пользователя",
    )

    access_token = models.CharField(
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
