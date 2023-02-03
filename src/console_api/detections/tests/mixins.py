"""Mixins for tests"""

from django.test import TestCase, Client

from console_api.detections.models import Detection
from console_api.test_utils import get_authorization_token


class DetectionListViewTestsMixin(TestCase):
    """Mixin for DetectionListView tests"""

    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(cls._DETECTIONS_COUNT):
            Detection.objects.create(
                source=f"Source {i}",
                source_message=f"Source message {i}",
                source_event={"test": i},
                details={"info": i},
                indicator_id="40434628-a47a-49c8-8adf-73e66b2b02e5",
                detection_event={"info": i},
                detection_message=f"Detection message {i}",
                tags_weight=i,
                indicator_weight=i,
            )

        cls.client = Client()

        cls.token = get_authorization_token(cls.client)

    def get_auth_get_response(self, url: str):
        """Return authorized GET response"""

        return self.client.get(url, HTTP_AUTHORIZATION=self.token)
