"""Mixins for tests"""

from django.test import TestCase, Client

from console_api.audit_logs.models import AuditLogs
from console_api.test_utils import get_authorization_token


class AuditLogsViewTestsMixin(TestCase):
    """Mixin for AuditLogsView tests"""

    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(cls._AUDIT_LOGS_COUNT):
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
        AuditLogs.objects.get(service_name="Console API token").delete()

    def get_auth_get_response(self, url: str):
        """Return authorized GET response"""

        return self.client.get(url, HTTP_AUTHORIZATION=self.token)
