from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from console_api.apps.models.abstract import BaseModel
from console_api.apps.indicator.models import Indicator
from console_api.apps.common.enums import (
    TypesEnum, FeedFormatEnum, AuthEnum, PollingFrequencyEnum, StatusUpdateEnum
)


FEED_STATUSES = (
    ("failed_to_update", "failed-to-update"),
    ("is_loading", "is-loading"),
    ("normal", "normal"),
)


class ParsingRule(BaseModel):
    """
    Модель правила для парсинга (CSV)
    """

    class Meta:
        verbose_name = "Правило парсинга"
        verbose_name_plural = "Правила парсинга"


class Feed(BaseModel):
    """Фид - источник данных"""

    title = models.TextField(
        "Название Фида",
        unique=True,
    )

    provider = models.TextField(
        "Название поставщика Фида",
    )

    description = models.TextField(
        "Описание Фида",
        null=True,
        blank=True,
    )

    format = models.TextField(
        "Формат фида",
        default=FeedFormatEnum.TXT_FILE.value,
    )

    certificate = models.TextField(
        "Файл сертификат",
        blank=True,
        null=True,
    )

    url = models.CharField(
        "Ссылка на файл Фида",
        max_length=255,
    )

    auth_type = models.TextField(
        "Формат фида",
        help_text="Например: http-basic, api-token",
        null=True,
        blank=True,
    )

    auth_api_token = models.TextField(
        "API токен",
    )

    auth_login = models.TextField(
        "Логин HTTP Basic Auth",
    )

    auth_pass = models.TextField(
        "Пароль HTTP Basic Auth",
    )

    certificate = models.BinaryField(
        "Сертификат",
    )

    use_taxii = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )

    polling_frequency = models.TextField(
        "Частота обновления",
        help_text="Формат CronTab",
        # TODO: Добавить Regex
    )

    weight = models.DecimalField(
        "Вес фида",
        decimal_places=3,
        max_digits=12,
    )

    available_fields = models.JSONField(
        "Список доступных полей в индикаторах фида",
    )

    parsing_rules = models.JSONField(
        "Настройки парсинга",
        null=True,
        blank=True,
    )

    status = models.TextField(
        "Статус фида",
        choices=FEED_STATUSES,
    )

    is_active = models.BooleanField(
        "Включен ли фид?",
        # TODO: уточнить default значение
        default=False,
    )

    is_truncating = models.BooleanField(
        "Включено ли обрезание фида?",
        # TODO: уточнить default значение
        default=False,
    )

    max_records_count = models.DecimalField(
        decimal_places=3,
        max_digits=12,
    )

    def __str__(self) -> str:
        return str(self.title)

    @classmethod
    def get_model_fields(cls):
        return [i.attname for i in cls._meta.fields]

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Фид"
        verbose_name_plural = "Фиды"

        db_table = "feeds"
