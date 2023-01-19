from django.db import models

from console_api.feed.models import IndicatorFeedRelationship, Feed


class History(models.Model):
    """SearchHistory - data source"""

    id = models.BigAutoField(
        primary_key=True,
    )

    search_type = models.CharField(
        "Тип поиска",
        max_length=64
    )

    query_text = models.CharField(
        "Содержимое текстового запроса",
        max_length=255
    )

    query_data = models.BinaryField(
        "Содержимое файлового запроса"
    )

    results = models.JSONField(
        "Результаты поиска"
    )

    created_at = models.DateTimeField(
        "Дата и время поиска",
        auto_now_add=True,
    )

    created_by = models.BigIntegerField(
        "Кто запросил поиск"
    )


class Indicator(models.Model):
    """Indicator"""

    id = models.UUIDField(
        primary_key=True,
    )

    ioc_type = models.CharField(
        "Тип индикатора",
        max_length=32,
    )

    value = models.CharField(
        "Значение индикатора",
        max_length=1024,
    )

    context = models.JSONField(
        "Данные контекста из Фидов и из Сервисов Обогащения Информацией",
    )

    is_archived = models.BooleanField(
        "Статус архивирования",
        default=False,
    )

    @property
    def feeds(self) -> list:
        """Return list of feeds that linked with the indicator"""

        feeds_ids = [
            relationship.feed_id
            for relationship in IndicatorFeedRelationship.objects.filter(
                indicator_id=self.id,
            )
        ]

        return [
            {
                "id": feed_id,
                "name": Feed.objects.get(id=feed_id).title,
                "provider": Feed.objects.get(id=feed_id).provider
            } for feed_id in feeds_ids
        ]

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Индикатор"
        verbose_name_plural = "Индикаторы"

        db_table = "indicators"

        unique_together = ("ioc_type", "value")

