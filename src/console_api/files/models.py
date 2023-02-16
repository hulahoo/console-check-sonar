"""Models for search app"""

from django.db import models


class Files(models.Model):
    """Files"""

    id = models.BigAutoField(
        primary_key=True,
    )

    bucket = models.CharField(
        "Название корзины",
        max_length=64,
    )

    key = models.CharField(
        "Ключ как имя файла",
        max_length=255,
    )

    content = models.BinaryField(
        "Содержимое файлового запроса",
    )

    chunk = models.IntegerField(
        "Номер чанка",
    )

    created_at = models.DateTimeField(
        "Дата и время загрузки файла",
        auto_now_add=True,
    )

    created_by = models.BigIntegerField(
        "Кто загрузил файл",
    )

    is_deleted = models.BooleanField(
        "Файл удалён",
        default=False
    )

    deleted_at = models.DateTimeField(
        "Дата и время удаления файла",
    )

    deleted_by = models.BigIntegerField(
        "Кто удалил файл",
    )

    hash_md5 = models.CharField(
        "Значение MD5 хэша файла",
    )

    hash_sha1 = models.CharField(
        "Значение SHA1 хэша файла",
    )

    hash_sha256 = models.CharField(
        "Значение SHA256 хэша файла",
    )

    class Meta:
        """Metainformation about the model"""

        db_table = "files"
