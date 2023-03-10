"""Models for search app"""

from django.db import models


class History(models.Model):
    """History of search"""

    id = models.BigAutoField(
        primary_key=True,
    )

    search_type = models.CharField(
        "Тип поиска",
        max_length=64,
    )

    query_text = models.TextField(
        "Содержимое текстового запроса",
    )

    query_data = models.BinaryField(
        "Содержимое файлового запроса",
    )

    results = models.JSONField(
        "Результаты поиска",
    )

    created_at = models.DateTimeField(
        "Дата и время поиска",
        auto_now_add=True,
    )

    created_by = models.BigIntegerField(
        "Кто запросил поиск",
    )

    class Meta:
        ordering = ["-created_at"]
