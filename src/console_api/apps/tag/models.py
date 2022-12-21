"""Models for tag app"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from apps.models.abstract import BaseModel


class Tag(BaseModel):
    """Тег"""

    title = models.TextField(
        "Название тега",
        unique=True,
    )

    weight = models.DecimalField(
        "Вес тега",
        blank=True,
        null=True,
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        max_digits=6,
        decimal_places=3,
    )

    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        verbose_name="Кем создано",
    )

    deleted_at = models.DateTimeField(
        "Дата и время удаления",
        null=True,
        blank=True,
        editable=False,
    )

    def delete(self) -> None:
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.title} | {self.weight}"

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Тег"
        verbose_name_plural = "Теги"

        db_table = "tags"
