"""Test views.py file"""

from django.test import TestCase, Client

from console_api.audit_logs.models import AuditLogs
from console_api.audit_logs.tests.constants import AUDIT_LOGS_URL
from console_api.test_utils import get_authorization_token
from console_api.constants import DIFFERENT_VALUES, WRONG_PAGE_SIZE


class ListWithoutParamsTests(TestCase):
    """Test list of logs without parameters"""

    __OBJECTS_COUNT = 3

    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(cls.__OBJECTS_COUNT):
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

        self.assertEqual(response.data.get("count"), self.__OBJECTS_COUNT)
        self.assertEqual(response.data.get("next", ""), None)
        self.assertEqual(response.data.get("previous", ""), None)

        for i in range(self.__OBJECTS_COUNT):
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


class PaginationParametersTests(TestCase):
    """Test page-number and page-size parameters for logs list"""

    __OBJECTS_COUNT = 50

    __DEFAULT_PAGE_SIZE = 25

    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(cls.__OBJECTS_COUNT):
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

    def test_page_number_1(self) -> None:
        """Test page-number=1 parameter"""

        response = self.client.get(
            AUDIT_LOGS_URL,
            HTTP_AUTHORIZATION=self.token,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data.get("count"), self.__OBJECTS_COUNT)
        self.assertIn(
            f"{AUDIT_LOGS_URL}?page-number=2",
            response.data.get("next", ""),
        )

        self.assertEqual(response.data.get("previous", ""), None)

        self.assertEqual(
            len(response.data.get("results")),
            self.__DEFAULT_PAGE_SIZE,
        )

    def test_page_number_2(self) -> None:
        """Test page-number=2 parameter"""

        response = self.client.get(
            f"{AUDIT_LOGS_URL}?page-number=2",
            HTTP_AUTHORIZATION=self.token,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data.get("count"), self.__OBJECTS_COUNT)
        self.assertEqual(response.data.get("next", ""), None)

        self.assertIn(AUDIT_LOGS_URL, response.data.get("previous", ""))

        self.assertEqual(
            len(response.data.get("results")),
            self.__DEFAULT_PAGE_SIZE,
        )

    def test_page_size(self) -> None:
        """Test page-size parameter"""

        response = self.client.get(
            f"{AUDIT_LOGS_URL}?page-size=2",
            HTTP_AUTHORIZATION=self.token,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), self.__OBJECTS_COUNT)
        self.assertIn(
            f"{AUDIT_LOGS_URL}?page-number=2&page-size=2",
            response.data.get("next", ""),
        )
        self.assertEqual(response.data.get("previous", ""), None)
        self.assertEqual(len(response.data.get("results")), 2)

    def test_page_size_2(self) -> None:
        """Test page-size parameter for page-number=2"""

        response = self.client.get(
            f"{AUDIT_LOGS_URL}?page-number=2&page-size=2",
            HTTP_AUTHORIZATION=self.token,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), self.__OBJECTS_COUNT)
        self.assertIn(
            f"{AUDIT_LOGS_URL}?page-number=3&page-size=2",
            response.data.get("next", ""),
        )
        self.assertIn(
            f"{AUDIT_LOGS_URL}?page-size=2",
            response.data.get("previous", ""),
        )
        self.assertEqual(len(response.data.get("results")), 2)

    def test_wrong_page_number(self) -> None:
        """Test wrong page-number parameter"""

        for value in DIFFERENT_VALUES:
            response = self.client.get(
                f"{AUDIT_LOGS_URL}?page-number={value}",
                HTTP_AUTHORIZATION=self.token,
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.data.get("detail"), "Invalid page.")

    def test_wrong_page_size(self) -> None:
        """Test wrong page-size parameter"""

        for value in WRONG_PAGE_SIZE:
            with self.subTest(f"{value=}"):
                response = self.client.get(
                    f"{AUDIT_LOGS_URL}?page-size={value}",
                    HTTP_AUTHORIZATION=self.token,
                )

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.data.get("detail"),
                    "page-size parameter is wrong",
                )


class SortByTests(TestCase):
    """Test list with sort-by param"""

    __OBJECTS_COUNT = 10

    __SORT_BY_PARAMS = (
        "id", "-id",
        "service-name", "-service-name",
        "user-id", "-user-id",
        "user-name", "-user-name",
        "event-type", "-event-type",
        "object-type", "-object-type",
        "object-name", "-object-name",
        "description", "-description",
        "created-at", "-created-at",
    )

    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(cls.__OBJECTS_COUNT):
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

    def test_sort_by_correct_values(self) -> None:
        """Tests for sort-by parameter with correct values"""

        for param in self.__SORT_BY_PARAMS:
            with self.subTest(f"{param=}"):
                response = self.client.get(
                    f"{AUDIT_LOGS_URL}?sort-by={param}",
                    HTTP_AUTHORIZATION=self.token,
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    response.data.get("count"),
                    self.__OBJECTS_COUNT,
                )

                results = response.data.get("results")

                self.assertEqual(len(results), self.__OBJECTS_COUNT)

                if param.startswith("-"):
                    results_values = [res.get(param[1:]) for res in results]

                    self.assertEqual(
                        sorted(results_values, reverse=True),
                        results_values,
                    )
                else:
                    results_values = [res.get(param) for res in results]

                    self.assertEqual(sorted(results_values), results_values)

    def test_sort_by_incorrect_values(self) -> None:
        """Tests for sort-by parameter with incorrect values"""

        for param in DIFFERENT_VALUES:
            with self.subTest(f"{param=}"):
                response = self.client.get(
                    f"{AUDIT_LOGS_URL}?sort-by={param}",
                    HTTP_AUTHORIZATION=self.token,
                )

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.data.get("detail"),
                    "Wrong value for sort-by parameter",
                )
