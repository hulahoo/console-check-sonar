"""Models for statistics app"""

from django.db import models


class StatMatchedObjects(models.Model):
    """stat_matched_objects table"""

    indicator_id = models.UUIDField()

    created_at = models.DateTimeField(
        "Дата и время создания",
        auto_now_add=True,
    )

    class Meta:
        """Metainformation about the model"""

        db_table = "stat_matched_objects"
        ordering = ["-created_at"]


class StatCheckedObjects(models.Model):
    """stat_checked_objects table"""

    created_at = models.DateTimeField(
        "Дата и время создания",
        auto_now_add=True,
    )

    class Meta:
        """Metainformation about the model"""

        db_table = "stat_checked_objects"
        ordering = ["-created_at"]
