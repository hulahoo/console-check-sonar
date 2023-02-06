"""Models for context_sources app"""

from django.db.models import (
    BigIntegerField,
    CharField,
    DateTimeField,
    Model,
    TextField,
)


IOC_TYPES = (
    ("ip", "ip"),
    ("domain", "domain"),
    ("hash", "hash"),
)


class ContextSources(Model):
    """Information enrichment services"""

    ioc_type = CharField(
        "Тип индикатора",
        max_length=32,
        choices=IOC_TYPES,
        default="ip",
    )

    source_url = CharField(
        "Ссылка на источник получения информации",
        max_length=255,
    )

    request_method = CharField(
        "HTTP-метод к запросу",
        max_length=16,
        default="get",
    )

    request_headers = TextField(
        "HTTP-заголовок к запросу",
        null=True,
    )

    request_body = TextField(
        "Тело HTTP-запроса",
        null=True,
    )

    inbound_removable_prefix = CharField(
        "Stripping. Удаляемый префикс",
        max_length=128,
        null=True,
    )

    outbound_appendable_prefix = CharField(
        "Wrapping. Название ключа контекста, куда мы помещаем результат ответа",
        max_length=128,
        null=True,
    )

    created_at = DateTimeField(
        "Дата и время добавления сервиса",
        auto_now_add=True,
    )

    created_by = BigIntegerField(
        "ID пользователя, создавшего сервис",
        null=True,
    )

    def __str__(self) -> str:
        return f"ContextSources ({self.id})"

    class Meta:
        """Metainformation about the model"""

        db_table = "context_sources"

        verbose_name = "Сервис обогащения информацией"
        verbose_name_plural = "Сервисы обогащения информацией"

        ordering = ["-created_at"]
