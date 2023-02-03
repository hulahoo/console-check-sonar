"""Test views.py file"""

import secrets

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from console_api.audit_logs.models import AuditLogs
from console_api.audit_logs.serializers import AuditLogsListSerializer
from console_api.audit_logs.tests.constants import AUDIT_LOGS_URL
from console_api.audit_logs.tests.mixins import AuditLogsViewTestsMixin
from console_api.audit_logs.views import AuditLogsListView
from console_api.constants import (
    DIFFERENT_VALUES,
    PAGE_NUMBER,
    PAGE_SIZE,
    SORT_BY,
    WRONG_PAGE_SIZE,
)
from console_api.services import CustomTokenAuthentication


class AuditLogsListViewFieldsTests(AuditLogsViewTestsMixin):
    """Test fields for AuditLogsListView"""

    _AUDIT_LOGS_COUNT = 3

    def test_authentication_classes(self) -> None:
        """Test authentication_classes field"""

        self.assertEqual(
            AuditLogsListView.authentication_classes,
            [CustomTokenAuthentication],
        )

    def test_permission_classes(self) -> None:
        """Test permission_classes field"""

        self.assertEqual(
            AuditLogsListView.permission_classes,
            [IsAuthenticated],
        )

    def test_queryset(self) -> None:
        """Test queryset field"""

        self.assertEqual(
            [log.id for log in AuditLogsListView().get_queryset()],
            [log.id for log in AuditLogs.objects.all()],
        )

    def test_serializer_class(self) -> None:
        """Test serializer_class field"""

        self.assertEqual(
            AuditLogsListView.serializer_class,
            AuditLogsListSerializer,
        )

    def test_mro(self) -> None:
        """Test MRO"""

        self.assertIn(ListAPIView, AuditLogsListView.mro())

    def test_sort_by_params(self) -> None:
        """Test __SORT_BY_PARAMS field"""

        expected_sort_by_params = (
            "id",
            "-id",
            "service_name",
            "-service_name",
            "user_id",
            "-user_id",
            "user_name",
            "-user_name",
            "event_type",
            "-event_type",
            "object_type",
            "-object_type",
            "object_name",
            "-object_name",
            "description",
            "-description",
            "created_at",
            "-created_at",
        )

        self.assertEqual(
            AuditLogsListView()._SORT_BY_PARAMS,
            expected_sort_by_params,
        )


class AuditLogsListViewWithoutParamsTests(AuditLogsViewTestsMixin):
    """Test AuditLogsListView without parameters"""

    _AUDIT_LOGS_COUNT = 3

    def test_list(self) -> None:
        """Test list of logs"""

        response = self.get_auth_get_response(AUDIT_LOGS_URL)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data.get("count"), self._AUDIT_LOGS_COUNT)
        self.assertEqual(response.data.get("next", ""), None)
        self.assertEqual(response.data.get("previous", ""), None)

        for i in range(self._AUDIT_LOGS_COUNT):
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


class AuditLogsListViewPaginationParametersTests(AuditLogsViewTestsMixin):
    """Test page-number and page-size parameters for AuditLogsListView"""

    _AUDIT_LOGS_COUNT = 50

    __DEFAULT_PAGE_SIZE = 25

    def test_page_number_1(self) -> None:
        """Test for page-number = 1"""

        response = self.get_auth_get_response(AUDIT_LOGS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), self._AUDIT_LOGS_COUNT)
        self.assertEqual(response.data.get("previous", ""), None)

        self.assertIn(
            f"{AUDIT_LOGS_URL}?{PAGE_NUMBER}=2",
            response.data.get("next", ""),
        )

        self.assertEqual(
            len(response.data.get("results")),
            self.__DEFAULT_PAGE_SIZE,
        )

    def test_page_number_2(self) -> None:
        """Test for page-number = 2"""

        response = self.get_auth_get_response(
            f"{AUDIT_LOGS_URL}?{PAGE_NUMBER}=2",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("next", ""), None)
        self.assertIn(AUDIT_LOGS_URL, response.data.get("previous", ""))
        self.assertEqual(response.data.get("count"), self._AUDIT_LOGS_COUNT)

        self.assertEqual(
            len(response.data.get("results")),
            self.__DEFAULT_PAGE_SIZE,
        )

    def test_page_size_2(self) -> None:
        """Test for page-size = 2"""

        response = self.get_auth_get_response(
            f"{AUDIT_LOGS_URL}?{PAGE_SIZE}=2",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), self._AUDIT_LOGS_COUNT)
        self.assertIn(
            f"{AUDIT_LOGS_URL}?{PAGE_NUMBER}=2&{PAGE_SIZE}=2",
            response.data.get("next", ""),
        )
        self.assertEqual(response.data.get("previous", ""), None)
        self.assertEqual(len(response.data.get("results")), 2)

    def test_page_size_page_number_2(self) -> None:
        """Test for page-size = 2 and page-number = 2"""

        response = self.get_auth_get_response(
            f"{AUDIT_LOGS_URL}?{PAGE_NUMBER}=2&{PAGE_SIZE}=2",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), self._AUDIT_LOGS_COUNT)
        self.assertIn(
            f"{AUDIT_LOGS_URL}?{PAGE_NUMBER}=3&{PAGE_SIZE}=2",
            response.data.get("next", ""),
        )
        self.assertIn(
            f"{AUDIT_LOGS_URL}?{PAGE_SIZE}=2",
            response.data.get("previous", ""),
        )
        self.assertEqual(len(response.data.get("results")), 2)

    def test_wrong_page_number(self) -> None:
        """Test wrong page-number parameter"""

        for value in DIFFERENT_VALUES:
            with self.subTest(f"{value=}"):
                response = self.get_auth_get_response(
                    f"{AUDIT_LOGS_URL}?{PAGE_NUMBER}={value}",
                )

                self.assertEqual(response.status_code, 404)
                self.assertEqual(response.data.get("detail"), "Invalid page.")

    def test_wrong_page_size(self) -> None:
        """Test wrong page-size parameter"""

        for value in WRONG_PAGE_SIZE:
            with self.subTest(f"{value=}"):
                response = self.get_auth_get_response(
                    f"{AUDIT_LOGS_URL}?{PAGE_SIZE}={value}",
                )

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.data.get("detail"),
                    "Invalid page-size parameter",
                )


class AuditLogsListViewSortByTests(AuditLogsViewTestsMixin):
    """Test sort-by param for AuditLogsListView"""

    __SORT_BY_PARAMS = (
        "id",
        "-id",
        "service-name",
        "-service-name",
        "user-id",
        "-user-id",
        "user-name",
        "-user-name",
        "event-type",
        "-event-type",
        "object-type",
        "-object-type",
        "object-name",
        "-object-name",
        "description",
        "-description",
        "created-at",
        "-created-at",
    )

    _AUDIT_LOGS_COUNT = 10

    def test_sort_by_correct_values(self) -> None:
        """Tests for sort-by parameter with correct values"""

        for param in self.__SORT_BY_PARAMS:
            with self.subTest(f"{param=}"):
                response = self.get_auth_get_response(
                    f"{AUDIT_LOGS_URL}?{SORT_BY}={param}",
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(
                    response.data.get("count"),
                    self._AUDIT_LOGS_COUNT,
                )

                results = response.data.get("results")

                self.assertEqual(len(results), self._AUDIT_LOGS_COUNT)

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
                response = self.get_auth_get_response(
                    f"{AUDIT_LOGS_URL}?{SORT_BY}={param}",
                )

                self.assertEqual(response.status_code, 400)
                self.assertEqual(
                    response.data.get("detail"),
                    f"Wrong value for {SORT_BY} parameter",
                )


class AuditLogsListViewFiltersTests(AuditLogsViewTestsMixin):
    """Test filters parameters for AuditLogsListView"""

    _AUDIT_LOGS_COUNT = 10

    def test_filter_not_exists_field_value(self) -> None:
        """Filter logs by not exists field value and should return 0 entries"""

        fields_and_values = {
            "id": 100,
            "service-name": "Not exists service name",
            "user-id": 100,
            "user-name": "Not exists user name",
            "event-type": "Not exists event type",
            "object-type": "Not exists object type",
            "object-name": "Not exists object name",
            "description": "Not exists description",
            "created-at": "2026-12-14T02:00:00.000Z",
        }

        for field, value in fields_and_values.items():
            with self.subTest(f"{field=}, {value=}"):
                response = self.get_auth_get_response(
                    f"{AUDIT_LOGS_URL}?filter[{field}]={value}",
                )

                results = response.data.get("results")

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data.get("count"), 0)
                self.assertEqual(response.data.get("next", ""), None)
                self.assertEqual(response.data.get("previous", ""), None)
                self.assertEqual(results, [])

    def test_filter_exists_field_value(self) -> None:
        """Filter logs by exists field value and should return 1 entry"""

        log_number = secrets.randbelow(self._AUDIT_LOGS_COUNT - 1)
        log_created_at = AuditLogs.objects.get(user_id=log_number).created_at

        fields_and_values = {
            "id": AuditLogs.objects.get(user_id=log_number).id,
            "service-name": f"Service name {log_number}",
            "user-id": log_number,
            "user-name": f"User name {log_number}",
            "event-type": f"Event type {log_number}",
            "object-type": f"Object type {log_number}",
            "object-name": f"Object name {log_number}",
            "description": f"Description {log_number}",
            "created-at": log_created_at.strftime("%Y-%m-%d %H:%M:%S.%f"),
        }

        for field, value in fields_and_values.items():
            with self.subTest(f"{field=}, {value=}"):
                response = self.get_auth_get_response(
                    f"{AUDIT_LOGS_URL}?filter[{field}]={value}",
                )

                results = response.data.get("results")

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data.get("count"), 1)
                self.assertEqual(response.data.get("next", ""), None)
                self.assertEqual(response.data.get("previous", ""), None)
                self.assertEqual(len(results), 1)

    def test_wrong_fields_values(self) -> None:
        """Filter logs by wrong fields values should return 400 error"""

        for field in "id", "user-id", "created-at":
            with self.subTest(f"{field=}"):
                response = self.get_auth_get_response(
                    f"{AUDIT_LOGS_URL}?filter[{field}]=value",
                )

                self.assertEqual(response.status_code, 400)


class AuditLogsListViewDoubleFiltersTests(AuditLogsViewTestsMixin):
    """Test double filters parameters for AuditLogsListView"""

    _AUDIT_LOGS_COUNT = 0

    def test_double_filters(self) -> None:
        """Filter logs by double params"""

        for i in range(3):
            AuditLogs.objects.create(
                service_name="Service name",
                user_id=1,
                user_name="User name",
                event_type="Event type",
                object_type="Object type",
                object_name="Object name",
                description="Description",
                prev_value={"test": i},
                new_value={"test": i},
                context={"info": f"INFO {i}"},
            )

        for i in range(3, 8):
            AuditLogs.objects.create(
                service_name="Service name",
                user_id=i,
                user_name=f"User name {i}",
                event_type=f"Event type {i}",
                object_type="Object type",
                object_name=f"Object name {i}",
                description=f"Description {i}",
                prev_value={"test": i},
                new_value={"test": i},
                context={"info": f"INFO {i}"},
            )

        filter_service_name = "filter[service-name]=Service name"
        filter_object_type = "filter[object-type]=Object type"

        filter_user_id = "filter[user-id]=1"
        filter_user_name = "filter[user-name]=User name"
        filter_event_type = "filter[event-type]=Event type"
        filter_object_name = "filter[object-name]=Object name"
        filter_description = "filter[description]=Description"

        filters = (
            filter_service_name + "&" + filter_user_id,
            filter_service_name + "&" + filter_user_name,
            filter_service_name + "&" + filter_event_type,
            filter_service_name + "&" + filter_object_name,
            filter_service_name + "&" + filter_description,

            filter_object_type + "&" + filter_user_id,
            filter_object_type + "&" + filter_user_name,
            filter_object_type + "&" + filter_event_type,
            filter_object_type + "&" + filter_object_name,
            filter_object_type + "&" + filter_description,
        )

        for filter_ in filters:
            with self.subTest(f"{filter_=}"):
                response = self.get_auth_get_response(
                    f"{AUDIT_LOGS_URL}?{filter_}",
                )

                results = response.data.get("results")

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data.get("count"), 3)
                self.assertEqual(response.data.get("next", ""), None)
                self.assertEqual(response.data.get("previous", ""), None)
                self.assertEqual(len(results), 3)
