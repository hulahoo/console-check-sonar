"""Models for statistics app"""

from django.db import models

from console_api.apps.models.abstract import CreationDateTimeField


class StatMatchedObjects(models.Model):
    """stat_matched_objects table"""

    indicator_id = models.UUIDField()

    created_at = CreationDateTimeField(
        "Создано",
    )

    class Meta:
        """Metainformation about the model"""

        db_table = "stat_matched_objects"


class StatCheckedObjects(models.Model):
    """stat_checked_objects table"""

    created_at = CreationDateTimeField(
        "Создано",
    )

    class Meta:
        """Metainformation about the model"""

        db_table = "stat_checked_objects"
