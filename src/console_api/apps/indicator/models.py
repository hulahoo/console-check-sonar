from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.tag.models import Tag
from apps.common.enums import TypesEnum
from apps.models.abstract import BaseModel


class Indicator(BaseModel):
    """
    Модель индикатора.
    """

    type = models.CharField(
        "Тип индикатора", max_length=13, default=TypesEnum.IP.value
    )
    uuid = models.CharField(
        "Уникальный идентификатор индикатора", unique=True, max_length=255
    )
    category = models.CharField(
        "Категория индикатора", max_length=128, blank=True, null=True
    )
    value = models.CharField("Значение индикатора", max_length=256)
    weight = models.IntegerField(
        "Вес", validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    tag = models.ManyToManyField(Tag, "tags")
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
        db_table = "sessions"
