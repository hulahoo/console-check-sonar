"""Test models.py file"""

from datetime import datetime

from django.db.models import (
    BigAutoField,
    BigIntegerField,
    CharField,
    DateTimeField,
    JSONField,
    Model,
)
from django.test import TestCase

from console_api.audit_logs.models import AuditLogs
from console_api.services import run_field_attribute_test


class AuditLogsTests(TestCase):
    """Test AuditLogs model"""

    @classmethod
    def setUpTestData(cls) -> None:
        AuditLogs.objects.create(
            service_name="Service name",
            user_id=1,
            user_name="User name",
            event_type="Event type",
            object_type="Object type",
            object_name="Object name",
            description="Description",
            prev_value={"test": 1},
            new_value={"test": 2},
            context={"info": "INFO"},
            created_at=datetime(2022, 11, 11),
        )

        cls.field_ant_type = {
            "id": BigAutoField,
            "service_name": CharField,
            "user_id": BigIntegerField,
            "user_name": CharField,
            "event_type": CharField,
            "object_type": CharField,
            "object_name": CharField,
            "description": CharField,
            "prev_value": JSONField,
            "new_value": JSONField,
            "context": JSONField,
            "created_at": DateTimeField,
        }

        cls.field_and_verbose_name = {
            "service_name": "Название сервиса или таблицы",
            "user_id": "ID пользователя",
            "user_name": "Имя пользователя",
            "event_type": "Тип события",
            "object_type": "Тип обьекта",
            "object_name": "Название обьекта",
            "description": "Описание операции",
            "prev_value": "Прошлое значение",
            "new_value": "Новое значение",
            "context": "Дополнительная информация",
            "created_at": "Дата и время записи действия",
        }

        cls.field_and_max_length = {
            "service_name": 128,
            "user_name": 256,
            "event_type": 128,
            "object_type": 128,
            "object_name": 128,
            "description": 256,
        }

        cls.field_and_auto_now_add = {
            "created_at": True,
        }

        cls.field_and_primary_key = {
            "id": True,
            "service_name": False,
            "user_id": False,
            "user_name": False,
            "event_type": False,
            "object_type": False,
            "object_name": False,
            "description": False,
            "prev_value": False,
            "new_value": False,
            "context": False,
            "created_at": False,
        }

    def test_verbose_name(self) -> None:
        """Test verbose_name attribute for fields"""

        run_field_attribute_test(
            AuditLogs,
            self,
            self.field_and_verbose_name,
            "verbose_name",
        )

    def test_max_length(self) -> None:
        """Test max_length attribute for fields"""

        run_field_attribute_test(
            AuditLogs,
            self,
            self.field_and_max_length,
            "max_length",
        )

    def test_auto_now_add(self) -> None:
        """Test auto_now_add attribute for fields"""

        run_field_attribute_test(
            AuditLogs,
            self,
            self.field_and_auto_now_add,
            "auto_now_add",
        )

    def test_primary_key(self) -> None:
        """Test primary_key attribute for fields"""

        run_field_attribute_test(
            AuditLogs,
            self,
            self.field_and_primary_key,
            "primary_key",
        )

    def test_fields_types(self) -> None:
        """Test types for fields"""

        for field, expected_type in self.field_ant_type.items():
            real_type = AuditLogs._meta.get_field(field).__class__

            self.assertEqual(real_type, expected_type)

    def test_model_mro(self) -> None:
        """Test AuditLogs MRO"""

        self.assertIn(Model, AuditLogs.mro())

    def test_model_verbose_name(self) -> None:
        """Test AuditLogs verbose_name"""

        self.assertEqual(
            AuditLogs._meta.verbose_name,
            "Журнал действий пользователя",
        )

    def test_model_verbose_name_plural(self) -> None:
        """Test AuditLogs verbose_name_plural"""

        self.assertEqual(
            AuditLogs._meta.verbose_name_plural,
            "Журналы действий пользователя",
        )

    def test_model_ordering(self) -> None:
        """Test AuditLogs ordering"""

        self.assertEqual(AuditLogs._meta.ordering, ["service_name"])

    def test_db_table(self) -> None:
        """Test AuditLogs db_table"""

        self.assertEqual(AuditLogs._meta.db_table, "audit_logs")
