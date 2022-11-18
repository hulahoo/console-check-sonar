from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from src.models.abstract import BaseModel
from src.indicator.models import Indicator
from src.common.enums import (
    TypesEnum, FeedFormatEnum, AuthEnum, PollingFrequencyEnum, StatusUpdateEnum
)


class ParsingRule(BaseModel):
    """
    Модель правила для парсинга (CSV)
    """

    class Meta:
        verbose_name = "Правило парсинга"
        verbose_name_plural = "Правила парсинга"


class Feed(BaseModel):
    """
    Модель фида - источника данных.
    """

    type_of_feed = models.CharField(
        "Тип фида", max_length=13, choices=TypesEnum.choices(), default=TypesEnum.IP
    )
    format_of_feed = models.CharField(
        "Формат фида", max_length=15, choices=FeedFormatEnum.choices(), default=FeedFormatEnum.TXT_FILE
    )
    auth_type = models.CharField(
        "Тип авторизации", max_length=7, choices=AuthEnum.choices(), default=AuthEnum.NO_AUTH
    )
    polling_frequency = models.CharField(
        "Частота обновления фида",
        max_length=17,
        choices=PollingFrequencyEnum.choices(),
        default=PollingFrequencyEnum.NEVER,
    )

    auth_login = models.CharField(
        "Логин для авторизации", max_length=32, blank=True, null=True
    )
    auth_password = models.CharField(
        "Пароль для авторизации", max_length=64, blank=True, null=True
    )
    ayth_querystring = models.CharField(
        "Строка для авторизации", max_length=128, blank=True, null=True
    )
    separator = models.CharField(
        "Разделитель для CSV формата", max_length=8, blank=True, null=True
    )
    parsing_rules = models.ManyToManyField(
        ParsingRule,
        verbose_name="Правила для парсинга",
        related_name="feed_parsing_rules",
        blank=True,
    )
    custom_field = models.CharField(
        "Кастомное поле", max_length=128, blank=True, null=True
    )
    sertificate = models.FileField("Файл сертификат", blank=True, null=True)
    vendor = models.CharField("Вендор", max_length=32)
    name = models.CharField("Название фида", max_length=32, unique=True)
    link = models.CharField("Ссылка на фид", max_length=255)
    confidence = models.IntegerField(
        "Достоверность", validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    records_quantity = models.IntegerField("Количество записей", blank=True, null=True)
    indicators = models.ManyToManyField(
        Indicator, related_name="feeds", verbose_name="Индикатор", blank=True
    )

    update_status = models.CharField(
        max_length=15, choices=StatusUpdateEnum.choices(), default=StatusUpdateEnum.ENABLED
    )

    ts = models.DateTimeField(auto_now_add=True)

    source = models.ForeignKey("source.Source", on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def get_model_fields(cls):
        return [i.attname for i in cls._meta.fields]

    class Meta:
        verbose_name = "Фид"
        verbose_name_plural = "Фиды"
