"""Utils for tests"""

from django.test import TestCase

from console_api.users.models import User
from console_api.constants import ADMIN_PASS_HASH, ADMIN_LOGIN, ADMIN_PASSWORD


class TestURLMixin(TestCase):
    """Mixin for testing status code"""

    def _test_url(
            self, path: str, expected_status_code=200,
            is_authorized=True, data=None) -> None:
        """Test status code if user is authorized"""

        token = self.__get_token() if is_authorized else ""

        if data:
            response = self.client.post(path, data, HTTP_AUTHORIZATION=token)
        else:
            response = self.client.get(path, HTTP_AUTHORIZATION=token)

        self.assertEqual(response.status_code, expected_status_code)

    def __get_token(self) -> str:
        """Return authorization token"""

        User.objects.create(
            login=ADMIN_LOGIN,
            password=ADMIN_PASS_HASH,
            full_name="admin",
            role="admin",
            is_active=True,
            staff=True,
            admin=True,
        )

        response = self.client.post(
            "/api/sessions",
            {
                "login": ADMIN_LOGIN,
                "password": ADMIN_PASSWORD,
            },
        )

        return f"Bearer {response.data.get('access-token')}"
