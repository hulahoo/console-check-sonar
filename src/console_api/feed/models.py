"""Models for feed app"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


FEED_STATUSES = (
    ("failed-to-update", "failed-to-update"),
    ("is-loading", "is-loading"),
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
    ("txt", "txt"),
    ("csv", "csv")
)


class Feed(models.Model):
    """Feed - data source"""

    title = models.CharField(
        "Название Фида",
        max_length=128,
        unique=True,
    )

    provider = models.CharField(
        "Название поставщика Фида",
        max_length=128
    )

    description = models.CharField(
        "Описание Фида",
        max_length=255,
        null=True,
        blank=True,
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
        max_length=255,
        null=True,
        blank=True,
    )

    auth_login = models.CharField(
        "Логин HTTP Basic Auth",
        max_length=32,
        null=True,
        blank=True,
    )

    auth_pass = models.CharField(
        "Пароль HTTP Basic Auth",
        max_length=32,
        null=True,
        blank=True,
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
        null=True,
        blank=True,
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
        default="normal",
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
        default=None,
    )

    created_at = models.DateTimeField(
        "Дата и время создания",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Дата и время обновления",
        auto_now=True,
    )

    def __str__(self) -> str:
        return str(self.title)

    @property
    def indicators_count(self) -> int:
        """Return count of indicators for the feed"""

        return IndicatorFeedRelationship.objects.filter(
            feed_id=self.id,
        ).count()

    @classmethod
    def get_model_fields(cls) -> list:
        """Return fields of the model"""

        return [i.attname for i in cls._meta.fields]

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Фид"
        verbose_name_plural = "Фиды"

        db_table = "feeds"
        ordering = ["title"]


class IndicatorFeedRelationship(models.Model):
    """Custom ManyToMany relationship table for Indicator and Feed"""

    indicator_id = models.UUIDField()

    feed_id = models.BigIntegerField()

    created_at = models.DateTimeField(
        "Дата и время создания",
        auto_now_add=True,
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
