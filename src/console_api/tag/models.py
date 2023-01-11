"""Models for tag app"""

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Tag(models.Model):
    """Тег"""

    title = models.CharField(
        "Название тега",
        max_length=128,
        unique=True,
    )

    weight = models.DecimalField(
        "Вес тега",
        validators=[MaxValueValidator(100), MinValueValidator(0)],
        max_digits=6,
        decimal_places=3,
    )

    created_by = models.BigIntegerField(
        "Кем создано"
    )

    created_at = models.DateTimeField(
        "Дата и время создания",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Дата и время обновления",
        auto_now=True,
    )

    deleted_at = models.DateTimeField(
        "Дата и время удаления",
        null=True,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return f"{self.title} | {self.weight}"

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Тег"
        verbose_name_plural = "Теги"

        db_table = "tags"


class IndicatorTagRelationship(models.Model):
    """Custom ManyToMany relationship table for Indicator and Feed"""

    indicator_id = models.UUIDField()

    tag_id = models.BigIntegerField()

    created_at = models.DateTimeField(
        "Дата и время создания",
        auto_now_add=True,
    )

    class Meta:
        """Metainformation about the model"""

        verbose_name = "Связь индикатор-фид"
        verbose_name_plural = "Связи индикатор-фид"

        db_table = "indicator_tag_relationships"
