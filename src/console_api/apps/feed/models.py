"""Models for feed app"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from console_api.apps.models.abstract import BaseModel, CreationDateTimeField


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
        choices=FEED_FORMAT,
        default="txt",
    )

    url = models.TextField(
        "Ссылка на файл Фида",
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

    status = models.TextField(
        "Статус фида",
        choices=FEED_STATUSES,
    )

    is_active = models.BooleanField(
        "Включен ли фид?",
        default=True,
    )

    is_truncating = models.BooleanField(
        "Включено ли обрезание фида?",
        default=False,
    )

    max_records_count = models.DecimalField(
        decimal_places=5,
        max_digits=20,
    )

    indicators = models.ManyToManyField(
        "indicator.Indicator",
        blank=True,
        null=True,
        through="IndicatorFeedRelationship",
    )

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

    indicator = models.ForeignKey(
        "indicator.Indicator",
        on_delete=models.CASCADE,
    )

    feed = models.ForeignKey(
        "feed.Feed",
        on_delete=models.CASCADE,
    )

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
