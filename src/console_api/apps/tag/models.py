"""Models for tag app"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from console_api.apps.models.abstract import BaseModel, CreationDateTimeField


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

    indicators = models.ManyToManyField(
        "indicator.Indicator",
        blank=True,
        null=True,
        through="IndicatorTagRelationship",
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

    indicator = models.ForeignKey(
        "indicator.Indicator",
        on_delete=models.CASCADE,
    )

    tag = models.ForeignKey(
        "tag.Tag",
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

        db_table = "indicator_tag_relationships"
