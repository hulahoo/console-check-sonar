"""Test views.py file"""

from django.test import TestCase, Client

from console_api.audit_logs.tests.constants import AUDIT_LOGS_URL
from console_api.audit_logs.models import AuditLogs
from console_api.test_utils import get_authorization_token


class ListTests(TestCase):
    """Test list of logs"""

    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(3):
            AuditLogs.objects.create(
                service_name=f"Service name {i}",
                user_id=i,
                user_name=f"User name {i}",
                event_type=f"Event type {i}",
                object_type=f"Object type {i}",
                object_name=f"Object name {i}",
                description=f"Description {i}",
                prev_value={"test": i},
                new_value={"test": i},
                context={"info": f"INFO {i}"},
            )

        cls.client = Client()
        cls.token = get_authorization_token(cls.client)

    def test_list(self) -> None:
        """Test list of logs"""

        response = self.client.get(
            AUDIT_LOGS_URL,
            HTTP_AUTHORIZATION=self.token,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data.get("count"), 3)
        self.assertEqual(response.data.get("next", ""), None)
        self.assertEqual(response.data.get("previous", ""), None)

        for i in range(3):
            results = response.data.get("results")[i]

            self.assertEqual(results.get("service-name"), f"Service name {i}")
            self.assertEqual(results.get("user-id"), i)
            self.assertEqual(results.get("user-name"), f"User name {i}")
            self.assertEqual(results.get("event-type"), f"Event type {i}")
            self.assertEqual(results.get("object-type"), f"Object type {i}")
            self.assertEqual(results.get("object-name"), f"Object name {i}")
            self.assertEqual(results.get("description"), f"Description {i}")
            self.assertEqual(results.get("prev-value"), {"test": i})
            self.assertEqual(results.get("new-value"), {"test": i})
            self.assertEqual(results.get("context"), {"info": f"INFO {i}"})
            self.assertNotEqual(results.get("created-at"), None)
