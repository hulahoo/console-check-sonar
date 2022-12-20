from django.db import models

from apps.models.abstract import BaseModel


class Tag(BaseModel):
    """
    Модель тега.
    """

    title = models.CharField("Название тега", max_length=30)
    weight = models.IntegerField("Вес тега", max_length=10, blank=True, null=True)
    created_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return f"{self.title} | {self.weight}"

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        db_table = "tags"
