"""Test views.py file"""

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from console_api.context_sources.models import ContextSources
from console_api.context_sources.tests.constants import CONTEXT_SOURCES_URL
from console_api.context_sources.views import ContextSourcesView
from console_api.context_sources.tests.mixins import ContextSourcesViewTestsMixin
from console_api.constants import (
    DIFFERENT_VALUES,
    PAGE_NUMBER,
    PAGE_SIZE,
    WRONG_PAGE_SIZE,
)
from console_api.services import CustomTokenAuthentication


class ContextSourcesViewFieldsTests(ContextSourcesViewTestsMixin):
    """Test fields for ContextSourcesView"""

    _CONTEXT_SOURCES_COUNT = 3

    def test_authentication_classes(self) -> None:
        """Test authentication_classes field"""

        self.assertEqual(
            ContextSourcesView.authentication_classes,
            [CustomTokenAuthentication],
        )

    def test_permission_classes(self) -> None:
        """Test permission_classes field"""

        self.assertEqual(
            ContextSourcesView.permission_classes,
            [IsAuthenticated],
        )

    def test_queryset(self) -> None:
        """Test queryset field"""

        self.assertEqual(
            [log.id for log in ContextSourcesView().get_queryset()],
            [log.id for log in ContextSources.objects.all()],
        )

    def test_mro(self) -> None:
        """Test MRO"""

        self.assertIn(ModelViewSet, ContextSourcesView.mro())


class ContextSourcesViewWithoutParamsTests(ContextSourcesViewTestsMixin):
    """Test ContextSourcesView without parameters"""

    _CONTEXT_SOURCES_COUNT = 1

    def test_list(self) -> None:
        """Test list of logs"""

        response = self.get_auth_get_response(CONTEXT_SOURCES_URL)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data.get("count"), self._CONTEXT_SOURCES_COUNT)
        self.assertEqual(response.data.get("next", ""), None)
        self.assertEqual(response.data.get("previous", ""), None)

        for i in range(self._CONTEXT_SOURCES_COUNT):
            results = response.data.get("results")[i]

            self.assertEqual(results.get("ioc-type"), "ip")
            self.assertEqual(
                results.get("source-url"),
                "https://virustotal.com/api/get_ip_info?ip={value}",
            )
            self.assertEqual(results.get("request-method"), f"get {i}")
            self.assertEqual(
                results.get("request-headers"),
                "Authorization: Bearer MDM0MjM5NDc2MD",
            )
            self.assertEqual(results.get("request-body"), "test")
            self.assertEqual(results.get("inbound-removable-prefix"), "data")
            self.assertEqual(
                results.get("outbound-appendable-prefix"),
                "virustotal",
            )
            self.assertEqual(results.get("created-by"), i)

            self.assertNotEqual(results.get("created-at"), None)


class ContextSourcesViewPaginationParametersTests(ContextSourcesViewTestsMixin):
    """Test page-number and page-size parameters for ContextSourcesView"""

    _CONTEXT_SOURCES_COUNT = 50

    __DEFAULT_PAGE_SIZE = 25

    def test_page_number_1(self) -> None:
        """Test for page-number = 1"""

        response = self.get_auth_get_response(CONTEXT_SOURCES_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), self._CONTEXT_SOURCES_COUNT)
        self.assertEqual(response.data.get("previous", ""), None)

        self.assertIn(
            f"{CONTEXT_SOURCES_URL}?{PAGE_NUMBER}=2",
            response.data.get("next", ""),
        )

        self.assertEqual(
            len(response.data.get("results")),
            self.__DEFAULT_PAGE_SIZE,
        )

    def test_page_number_2(self) -> None:
        """Test for page-number = 2"""

        response = self.get_auth_get_response(
            f"{CONTEXT_SOURCES_URL}?{PAGE_NUMBER}=2",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("next", ""), None)
        self.assertIn(CONTEXT_SOURCES_URL, response.data.get("previous", ""))
        self.assertEqual(response.data.get("count"), self._CONTEXT_SOURCES_COUNT)

        self.assertEqual(
            len(response.data.get("results")),
            self.__DEFAULT_PAGE_SIZE,
        )

    def test_page_size_2(self) -> None:
        """Test for page-size = 2"""

        response = self.get_auth_get_response(
            f"{CONTEXT_SOURCES_URL}?{PAGE_SIZE}=2",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), self._CONTEXT_SOURCES_COUNT)
        self.assertIn(
            f"{CONTEXT_SOURCES_URL}?{PAGE_NUMBER}=2&{PAGE_SIZE}=2",
            response.data.get("next", ""),
        )
        self.assertEqual(response.data.get("previous", ""), None)
        self.assertEqual(len(response.data.get("results")), 2)

    def test_page_size_page_number_2(self) -> None:
        """Test for page-size = 2 and page-number = 2"""

        response = self.get_auth_get_response(
            f"{CONTEXT_SOURCES_URL}?{PAGE_NUMBER}=2&{PAGE_SIZE}=2",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), self._CONTEXT_SOURCES_COUNT)
        self.assertIn(
            f"{CONTEXT_SOURCES_URL}?{PAGE_NUMBER}=3&{PAGE_SIZE}=2",
            response.data.get("next", ""),
        )
        self.assertIn(
            f"{CONTEXT_SOURCES_URL}?{PAGE_SIZE}=2",
            response.data.get("previous", ""),
        )
        self.assertEqual(len(response.data.get("results")), 2)

    def test_wrong_page_number(self) -> None:
        """Test wrong page-number parameter"""

        for value in DIFFERENT_VALUES:
            with self.subTest(f"{value=}"):
                response = self.get_auth_get_response(
                    f"{CONTEXT_SOURCES_URL}?{PAGE_NUMBER}={value}",
                )

                self.assertEqual(response.status_code, 404)
                self.assertEqual(response.data.get("detail"), "Invalid page.")

    def test_wrong_page_size(self) -> None:
        """Test wrong page-size parameter"""

        for value in WRONG_PAGE_SIZE:
            with self.subTest(f"{value=}"):
                response = self.get_auth_get_response(
                    f"{CONTEXT_SOURCES_URL}?{PAGE_SIZE}={value}",
                )

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.data.get("detail"),
                    "Invalid page-size parameter",
                )
