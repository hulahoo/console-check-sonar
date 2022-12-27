"""Models for feed app"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from console_api.apps.models.abstract import BaseModel, CreationDateTimeField, ModificationDateTimeField


FEED_STATUSES = (
    ("failed_to_update", "failed-to-update"),
    ("is_loading", "is-loading"),
    ("normal", "normal"),
)

FEED_FORMAT = (
    ("json", "json"),
    ("stix_1", "stix-1"),
    ("stix_2", "stix-2"),
    ("misp", "misp"),
    ("csv", "csv"),
    ("txt", "txt"),
    ("xml", "xml"),
)


class Feed(BaseModel):
    """Feed - data source"""

    title = models.CharField(
        "Название Фида",
        max_length=128,
    )

    provider = models.CharField(
        "Название поставщика Фида",
        max_length=128
    )

    description = models.CharField(
        "Описание Фида",
        max_length=255
    )

    format = models.CharField(
        "Формат фида",
        max_length=8,
        choices=FEED_FORMAT,
    )

    url = models.CharField(
        "Ссылка на файл Фида",
        max_length=128
    )

    auth_type = models.CharField(
        "Формат фида",
        help_text="Например: http-basic, api-token",
        max_length=16
    )

    auth_api_token = models.CharField(
        "API токен",
        max_length=255
    )

    auth_login = models.CharField(
        "Логин HTTP Basic Auth",
        max_length=32
    )

    auth_pass = models.CharField(
        "Пароль HTTP Basic Auth",
        max_length=32
    )

    certificate = models.BinaryField(
        "Сертификат",
    )

    is_use_taxii = models.BooleanField(
        default=False,
    )

    polling_frequency = models.CharField(
        "Частота обновления",
        max_length=32,
        help_text="Формат CronTab",
    )

    weight = models.DecimalField(
        "Вес фида",
        decimal_places=3,
        max_digits=6,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
    )

    available_fields = models.JSONField(
        "Список доступных полей в индикаторах фида",
    )

    parsing_rules = models.JSONField(
        "Настройки парсинга",
        null=True,
        blank=True,
    )

    status = models.CharField(
        "Статус фида",
        max_length=32,
        choices=FEED_STATUSES,
    )

    is_active = models.BooleanField(
        "Включен ли фид?",
        default=True,
    )

    is_truncating = models.BooleanField(
        "Включено ли обрезание фида?",
        default=True,
    )

    max_records_count = models.DecimalField(
        decimal_places=5,
        max_digits=20,
    )

    updated_at = ModificationDateTimeField("Время изменения")

    def __str__(self) -> str:
        return str(self.title)

    @classmethod
    def get_model_fields(cls) -> list:
        """Return fields of the model"""

        return [i.attname for i in cls._meta.fields]

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Фид"
        verbose_name_plural = "Фиды"

        db_table = "feeds"


class IndicatorFeedRelationship(models.Model):
    """Custom ManyToMany relationship table for Indicator and Feed"""

    indicator_id = models.UUIDField()

    feed_id = models.BigIntegerField()

    created_at = CreationDateTimeField(
        "Дата и время создания связи",
    )

    deleted_at = models.DateTimeField(
        "Дата и время удаления связи",
        help_text="Если значение пустое, значит связь существующая",
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Связь индикатор-фид"
        verbose_name_plural = "Связи индикатор-фид"

        db_table = "indicator_feed_relationships"
