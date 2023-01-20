"""Models for source app"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


SOURCE_AUTH_TYPES = (
    ("no_auth", "NAU"),
    ("api", "API"),
    ("basic", "BSC"),
)

SOURCE_FORMATS = (
    ("stix", "STIX"),
    ("misp", "MISP"),
    ("free_text", "FREE_TEXT"),
    ("json", "JSON"),
    ("csv", "CSV"),
)


class Source(models.Model):
    """Source model"""

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    is_instead_full = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    provider_name = models.CharField(
        max_length=255,
    )

    path = models.TextField()

    certificate = models.FileField(
        "Путь к сертификату",
        blank=True,
        null=True,
    )

    authenticity = models.IntegerField(
        "Достоверность",
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        default=0,
    )

    format = models.CharField(
        "Формат",
        max_length=17,
        choices=SOURCE_FORMATS,
        default="CSV",
    )

    auth_type = models.CharField(
        "Тип авторизации",
        max_length=17,
        choices=SOURCE_AUTH_TYPES,
        default="NAU",
    )

    auth_login = models.CharField(
        "Логин для авторизации",
        max_length=32,
        blank=True,
        null=True,
    )

    auth_password = models.CharField(
        "Пароль для авторизации",
        max_length=64,
        blank=True,
        null=True,
    )

    max_rows = models.IntegerField(
        default=None,
        null=True,
    )

    raw_indicators = models.TextField(
        default=None,
        null=True,
    )

    update_time_period = models.PositiveBigIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        "Дата и время создания",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Дата и время обновления",
        auto_now=True,
    )

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Источник"
        verbose_name_plural = "Источники"
        ordering = ["-created_at"]
        db_table = "sources"
