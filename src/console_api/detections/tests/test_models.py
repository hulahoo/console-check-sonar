"""Test models.py file"""

from django.db.models import (
    BigAutoField,
    DateTimeField,
    DecimalField,
    JSONField,
    Model,
    TextField,
    UUIDField,
)
from django.test import TestCase
from django.core.validators import (
    DecimalValidator,
    MaxValueValidator,
    MinValueValidator,
)

from console_api.detections.models import Detection
from console_api.services import run_field_attribute_test


class DetectionTests(TestCase):
    """Test Detection model"""

    @classmethod
    def setUpTestData(cls) -> None:
        Detection.objects.create(
            source="Source",
            source_message="Source message",
            source_event={"test": 1},
            details={"info": "detail"},
            indicator_id="40434628-a47a-49c8-8adf-73e66b2b02e5",
            detection_event={"info": "event"},
            detection_message="Detection message",
            tags_weight=10,
            indicator_weight=10,
        )

        cls.field_ant_type = {
            "id": BigAutoField,
            "source": TextField,
            "source_message": TextField,
            "source_event": JSONField,
            "details": JSONField,
            "indicator_id": UUIDField,
            "detection_event": JSONField,
            "detection_message": TextField,
            "tags_weight": DecimalField,
            "indicator_weight": DecimalField,
            "created_at": DateTimeField,
        }

        cls.field_and_verbose_name = {
            "source": "Источник",
            "source_message": "Текст входящего сообщения от SIEM",
            "source_event": "Результат парсинга входящего сообщения от SIEM",
            "details": "Дополнительная информация",
            "indicator_id": "Обнаруженный Индикатор для данного события",
            "detection_event": "Объект с информацией об обнаружении",
            "detection_message": "Текст исходящего сообщения во внешнюю ИС (SIEM)",
            "tags_weight": "Вес тэгов Индикатора на момент обнаружения",
            "indicator_weight": "Вес Индикатора на момент обнаружения",
            "created_at": "Дата создания обнаружения",
        }

        cls.field_and_auto_now_add = {
            "created_at": True,
        }

        cls.field_and_primary_key = {
            "id": True,
            "source": False,
            "source_message": False,
            "source_event": False,
            "details": False,
            "indicator_id": False,
            "detection_event": False,
            "detection_message": False,
            "tags_weight": False,
            "indicator_weight": False,
            "created_at": False,
        }

        cls.field_and_decimal_places = {
            "tags_weight": 5,
            "indicator_weight": 5,
        }

        cls.field_and_max_digits = {
            "tags_weight": 8,
            "indicator_weight": 8,
        }

        cls.field_and_validators = {
            "tags_weight": [
                MinValueValidator(1),
                MaxValueValidator(100),
                DecimalValidator(8, 5),
            ],
        }

    def test_verbose_name(self) -> None:
        """Test verbose_name attribute for fields"""

        run_field_attribute_test(
            Detection,
            self,
            self.field_and_verbose_name,
            "verbose_name",
        )

    def test_decimal_places(self) -> None:
        """Test decimal_places attribute for fields"""

        run_field_attribute_test(
            Detection,
            self,
            self.field_and_decimal_places,
            "decimal_places",
        )

    def test_max_digits(self) -> None:
        """Test max_digits attribute for fields"""

        run_field_attribute_test(
            Detection,
            self,
            self.field_and_max_digits,
            "max_digits",
        )

    def test_validators(self) -> None:
        """Test validators attribute for fields"""

        run_field_attribute_test(
            Detection,
            self,
            self.field_and_validators,
            "validators",
        )

    def test_auto_now_add(self) -> None:
        """Test auto_now_add attribute for fields"""

        run_field_attribute_test(
            Detection,
            self,
            self.field_and_auto_now_add,
            "auto_now_add",
        )

    def test_primary_key(self) -> None:
        """Test primary_key attribute for fields"""

        run_field_attribute_test(
            Detection,
            self,
            self.field_and_primary_key,
            "primary_key",
        )

    def test_fields_types(self) -> None:
        """Test types for fields"""

        for field, expected_type in self.field_ant_type.items():
            real_type = Detection._meta.get_field(field).__class__

            self.assertEqual(real_type, expected_type)

    def test_model_mro(self) -> None:
        """Test Detection MRO"""

        self.assertIn(Model, Detection.mro())

    def test_model_verbose_name(self) -> None:
        """Test Detection verbose_name"""

        self.assertEqual(Detection._meta.verbose_name, "Обнаружение")

    def test_model_verbose_name_plural(self) -> None:
        """Test Detection verbose_name_plural"""

        self.assertEqual(Detection._meta.verbose_name_plural, "Обнаружения")

    def test_model_ordering(self) -> None:
        """Test Detection ordering"""

        self.assertEqual(Detection._meta.ordering, ["-created_at"])

    def test_db_table(self) -> None:
        """Test Detection db_table"""

        self.assertEqual(Detection._meta.db_table, "detections")

    def test_str(self) -> None:
        """Test __str__ method"""

        self.assertEqual(
            str(Detection.objects.last()),
            str(Detection.objects.last().id),
        )