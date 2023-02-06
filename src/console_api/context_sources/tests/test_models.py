"""Test models.py file"""

from django.db.models import (
    BigAutoField,
    BigIntegerField,
    CharField,
    DateTimeField,
    Model,
    TextField,
)
from django.test import TestCase

from console_api.context_sources.models import ContextSources
from console_api.services import run_field_attribute_test


class ContextSourcesTests(TestCase):
    """Test ContextSources model"""

    @classmethod
    def setUpTestData(cls) -> None:
        ContextSources.objects.create(
            ioc_type="ip",
            source_url="https://virustotal.com/api/get_ip_info?ip={value}",
            request_method="get",
            request_headers="Authorization: Bearer MDM0MjM5NDc2MD",
            request_body="test",
            inbound_removable_prefix="data",
            outbound_appendable_prefix="virustotal",
            created_by=1,
        )

        cls.field_ant_type = {
            "id": BigAutoField,
            "ioc_type": CharField,
            "source_url": CharField,
            "request_method": CharField,
            "request_headers": TextField,
            "request_body": TextField,
            "inbound_removable_prefix": CharField,
            "outbound_appendable_prefix": CharField,
            "created_at": DateTimeField,
            "created_by": BigIntegerField,
        }

        cls.field_and_verbose_name = {
            "ioc_type": "Тип индикатора",
            "source_url": "Ссылка на источник получения информации",
            "request_method": "HTTP-метод к запросу",
            "request_headers": "HTTP-заголовок к запросу",
            "request_body": "Тело HTTP-запроса",
            "inbound_removable_prefix": "Stripping. Удаляемый префикс",
            "outbound_appendable_prefix":
                "Wrapping. Название ключа контекста, куда мы помещаем "
                "результат ответа",
            "created_at": "Дата и время добавления сервиса",
            "created_by": "ID пользователя, создавшего сервис",
        }

        cls.field_and_max_length = {
            "ioc_type": 32,
            "source_url": 255,
            "request_method": 16,
            "inbound_removable_prefix": 128,
            "outbound_appendable_prefix": 128,
        }

        cls.field_and_auto_now_add = {
            "created_at": True,
        }

        cls.field_and_null = {
            "ioc_type": False,
            "source_url": False,
            "request_method": False,
            "request_headers": True,
            "request_body": True,
            "inbound_removable_prefix": True,
            "outbound_appendable_prefix": True,
            "created_at": True,
            "created_by": True,
        }

        cls.field_and_default = {
            "ioc_type": "ip",
            "request_method": "get",
        }

        cls.field_and_choices = {
            "ioc_type": (
                ("ip", "ip"),
                ("domain", "domain"),
                ("hash", "hash"),
            ),
        }

        cls.field_and_primary_key = {
            "id": True,
            "ioc_type": False,
            "source_url": False,
            "request_method": False,
            "request_headers": False,
            "request_body": False,
            "inbound_removable_prefix": False,
            "outbound_appendable_prefix": False,
            "created_at": False,
            "created_by": False,
        }

    def test_verbose_name(self) -> None:
        """Test verbose_name attribute for fields"""

        run_field_attribute_test(
            ContextSources,
            self,
            self.field_and_verbose_name,
            "verbose_name",
        )

    def test_max_length(self) -> None:
        """Test max_length attribute for fields"""

        run_field_attribute_test(
            ContextSources,
            self,
            self.field_and_max_length,
            "max_length",
        )

    def test_auto_now_add(self) -> None:
        """Test auto_now_add attribute for fields"""

        run_field_attribute_test(
            ContextSources,
            self,
            self.field_and_auto_now_add,
            "auto_now_add",
        )

    def test_choices(self) -> None:
        """Test choices attribute for fields"""

        run_field_attribute_test(
            ContextSources,
            self,
            self.field_and_choices,
            "choices",
        )

    def test_null(self) -> None:
        """Test null attribute for fields"""

        run_field_attribute_test(
            ContextSources,
            self,
            self.field_and_null,
            "null",
        )

    def test_default(self) -> None:
        """Test default attribute for fields"""

        run_field_attribute_test(
            ContextSources,
            self,
            self.field_and_default,
            "default",
        )

    def test_primary_key(self) -> None:
        """Test primary_key attribute for fields"""

        run_field_attribute_test(
            ContextSources,
            self,
            self.field_and_primary_key,
            "primary_key",
        )

    def test_fields_types(self) -> None:
        """Test types for fields"""

        for field, expected_type in self.field_ant_type.items():
            real_type = ContextSources._meta.get_field(field).__class__

            self.assertEqual(real_type, expected_type)

    def test_model_mro(self) -> None:
        """Test ContextSources MRO"""

        self.assertIn(Model, ContextSources.mro())

    def test_model_verbose_name(self) -> None:
        """Test ContextSources verbose_name"""

        self.assertEqual(
            ContextSources._meta.verbose_name,
            "Сервис обогащения информацией",
        )

    def test_model_verbose_name_plural(self) -> None:
        """Test ContextSources verbose_name_plural"""

        self.assertEqual(
            ContextSources._meta.verbose_name_plural,
            "Сервисы обогащения информацией",
        )

    def test_model_ordering(self) -> None:
        """Test ContextSources ordering"""

        self.assertEqual(ContextSources._meta.ordering, ["-created_at"])

    def test_db_table(self) -> None:
        """Test ContextSources db_table"""

        self.assertEqual(ContextSources._meta.db_table, "context_sources")

    def test_str(self) -> None:
        """Test __str__ method"""

        self.assertEqual(
            str(ContextSources.objects.last()),
            f"ContextSources ({ContextSources.objects.last().id})",
        )
