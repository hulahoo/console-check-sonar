from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from console_api.apps.models.abstract import BaseModel
from console_api.apps.common.enums import FormatTypeEnum, AuthEnum


class Source(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_instead_full = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    provider_name = models.CharField(max_length=255)
    path = models.TextField()
    certificate = models.FileField("Путь к сертификату", blank=True, null=True)
    authenticity = models.IntegerField(
        "Достоверность", validators=[MaxValueValidator(100), MinValueValidator(0)],
        default=0
    )
    format = models.CharField(
        "Формат", max_length=17, choices=FormatTypeEnum.choices(), default=FormatTypeEnum.CSV
    )

    auth_type = models.CharField(
        "Тип авторизации", max_length=17, choices=AuthEnum.choices(), default=AuthEnum.NO_AUTH
    )
    auth_login = models.CharField(
        "Логин для авторизации", max_length=32, blank=True, null=True
    )
    auth_password = models.CharField(
        "Пароль для авторизации", max_length=64, blank=True, null=True
    )

    max_rows = models.IntegerField(default=None, null=True)
    raw_indicators = models.TextField(default=None, null=True)
    update_time_period = models.PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'
        db_table = "sources"
