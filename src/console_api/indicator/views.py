"""Views for detections app"""
import requests
from typing import List
from datetime import datetime

from django.conf import settings
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from console_api.indicator.models import Indicator
from console_api.indicator.serializers import (
    IndicatorCreateSerializer,
    IndicatorDetailSerializer,
    IndicatorListSerializer,
)
from console_api.indicator.services import (
    create_indicator_activity,
    get_indicator_or_error_response,
)
from console_api.mixins import (
    get_boolean_from_str,
    get_filter_query_param,
    IndicatorQueryMixin
)
from console_api.services import (
    CustomTokenAuthentication,
    create_audit_log_entry,
    get_response_with_pagination,
    get_indicator_logging_data,
    get_sort_by_param,
)
from console_api.tag.models import Tag, IndicatorTagRelationship
from console_api.indicator.constants import LOG_SERVICE_NAME


class IndicatorsView(ModelViewSet, IndicatorQueryMixin):
    """/indicators endpoint view"""

    queryset = Indicator.objects.all()

    serializer_classes = {
        "list": IndicatorListSerializer,
        "create": IndicatorCreateSerializer,
    }

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        """Return response with list of indicators"""

        self.queryset = self.get_queryset()

        if is_archived := get_filter_query_param(request, "is-archived"):
            if is_archived := get_boolean_from_str(is_archived):
                self.queryset = self.queryset.filter(is_archived=is_archived)
            else:
                self.queryset = self.queryset.filter(
                    deleted_at=None,
                    is_archived=is_archived,
                )
        else:
            self.queryset = self.queryset.filter(deleted_at=None)

        self.add_queryset_filters(request=request)
        self.add_counter_queryset_filters(request=request)
        self.add_boolean_filters(request=request)
        self.add_weight_filters(request=request)
        self.add_queryset_at_time_filters(request=request)

        # tags and feed_name should be below others
        # self.add_tags_filters(request=request)
        self.add_feed_name_filters(request=request)
        self.__sort_queryset_by_param(request)

        return get_response_with_pagination(
            request,
            self.queryset,
            self.get_serializer,
        )

    def __sort_queryset_by_param(self, request: Request) -> None:
        """Sort the queryset by the given parameter"""

        if sort_by := get_sort_by_param(request):
            if sort_by == "ioc_weight":
                sort_by = "weight"
            elif sort_by == "-ioc_weight":
                sort_by = "-weight"

            self.queryset = self.queryset.order_by(sort_by)

    def get_serializer_class(self):
        """Return serializer class for the method"""

        return self.serializer_classes.get(self.action)

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Create an indicator"""

        if not request.data:
            return Response(
                {"detail": "Missing fields"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_create(serializer)

        create_audit_log_entry(request, {
            "table": LOG_SERVICE_NAME,
            "event_type": "create-indicator",
            "object_type": "indicator",
            "object_name": "Indicator",
            "description": "Create a new indicator",
            "new_value": request.data,
        })

        return Response(status=status.HTTP_201_CREATED)

    def get(self, request: Request, *args, **kwargs) -> Response:
        """Return response with list of indicators"""

        self.param_dict = {
            "start_period": request.GET.get("start-period-at"),
            "finish_period": request.GET.get("finish-period-at"),
        }

        return self.list(request, *args, **kwargs)


class MarkListAsNotFalsePositiveView(APIView):
    """Change is_false_positive field to False for list of indicators"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        indicators_ids = request.data.get("indicators", [])
        all_indicators = []

        for id_ in indicators_ids:
            indicator = get_indicator_or_error_response(id_)

            if isinstance(indicator, Response):
                return indicator

            all_indicators.append(indicator)

        for indicator in all_indicators:
            indicator.is_false_positive = False
            indicator.save()

        create_audit_log_entry(request, {
            "table": LOG_SERVICE_NAME,
            "event_type": "mark-indicators-list-as-not-false-positive",
            "object_type": "indicator",
            "object_name": "Indicator",
            "description": "Mark indicators list as not false positive",
        })

        return Response(status=status.HTTP_200_OK)


class MarkIndicatorAsFalsePositiveView(APIView):
    """Change is_false_positive field to True for the indicator"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        indicator_id = kwargs.get("indicator_id")
        indicator = get_indicator_or_error_response(indicator_id)

        if isinstance(indicator, Response):
            return indicator

        prev_indicator_value = get_indicator_logging_data(indicator)

        is_false_positive = request.POST.get("is-false-positive", "true")
        is_false_positive = get_boolean_from_str(is_false_positive)

        indicator.is_false_positive = is_false_positive
        indicator.save()

        create_indicator_activity({
            "indicator_id": indicator_id,
            "activity_type": "mark-indicator-as-false-positive",
            "created_by": request.user.id,
            "details": request.data.get("details"),
        })

        create_audit_log_entry(request, {
            "table": LOG_SERVICE_NAME,
            "event_type": "mark-indicator-as-false-positive",
            "object_type": "indicator",
            "object_name": "Indicator",
            "description": "Mark indicator as false positive",
            "prev_value": prev_indicator_value,
            "new_value": get_indicator_logging_data(indicator),
        })

        return Response(status=status.HTTP_200_OK)


class IndicatorDetailView(APIView):
    """View for detail of the indicator"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Change data of the indicator"""

        indicator_id = kwargs.get("indicator_id")
        indicator = get_indicator_or_error_response(indicator_id)

        if isinstance(indicator, Response):
            return indicator

        prev_indicator_value = get_indicator_logging_data(indicator)

        serializer = IndicatorDetailSerializer(indicator, data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        create_audit_log_entry(request, {
            "table": LOG_SERVICE_NAME,
            "event_type": "change-indicator",
            "object_type": "indicator",
            "object_name": "Indicator",
            "description": "Change indicator",
            "prev_value": prev_indicator_value,
            "new_value": get_indicator_logging_data(indicator),
        })

        return Response(status=status.HTTP_200_OK)

    def get(self, request: Request, *args, **kwargs) -> Response:
        """Return info about the indicator"""

        indicator_id = kwargs.get("indicator_id")
        indicator = get_indicator_or_error_response(indicator_id)

        if isinstance(indicator, Response):
            return indicator

        return Response(
            data=IndicatorDetailSerializer(indicator).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """Delete the indicator"""

        indicator_id = kwargs.get("indicator_id")
        indicator = get_indicator_or_error_response(indicator_id)

        if isinstance(indicator, Response):
            return indicator

        prev_indicator_value = get_indicator_logging_data(indicator)

        indicator.deleted_at = datetime.now()
        indicator.is_archived = True
        indicator.save()

        create_indicator_activity({
            "indicator_id": indicator_id,
            "activity_type": "Delete indicator",
            "created_by": request.user.id,
            "details": request.data.get("details"),
        })

        create_audit_log_entry(request, {
            "table": LOG_SERVICE_NAME,
            "event_type": "delete-indicator",
            "object_type": "indicator",
            "object_name": "Indicator",
            "description": "Delete indicator",
            "prev_value": prev_indicator_value,
            "new_value": get_indicator_logging_data(indicator),
        })

        return Response(status=status.HTTP_200_OK)


class ChangeIndicatorTagsView(APIView):
    """Change tags for the indicator"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Change tags for the indicator"""

        indicator_id = kwargs.get("indicator_id")
        indicator = get_indicator_or_error_response(indicator_id)

        if isinstance(indicator, Response):
            return indicator

        prev_indicator_value = get_indicator_logging_data(indicator)

        if not request.data.get("tags"):
            return Response(
                {"detail": "Tags not specified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tags = request.data.get("tags")
        tags = tags.replace("[", "").replace("]", "").replace(" ", "").split(",")

        if tags == ['']:
            tags = []

        if not all(tag.isdigit() for tag in tags):
            return Response(
                {"detail": "Tags not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_tags = [int(tag) for tag in tags if tag != ""]
        tags: List[Tag] = Tag.objects.get(id__in=new_tags)

        if len(new_tags) != tags:
            return Response(
                {"detail": "Tags wrong"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Indicator.objects.filter(id=indicator_id).exists():
            IndicatorTagRelationship.objects.filter(
                indicator_id=indicator_id,
            ).delete()
            indicator = Indicator.objects.get(id=indicator_id)
            indicator.tags_weight = sum(tag.weight for tag in tags)
            indicator.save()

            for tag in tags:
                IndicatorTagRelationship.objects.create(
                    indicator_id=indicator_id,
                    tag_id=tag.id,
                )

            create_indicator_activity({
                "indicator_id": indicator_id,
                "activity_type": "update-tags",
                "created_by": request.user.id,
                "details": request.data.get("details"),
            })

            create_audit_log_entry(request, {
                "table": LOG_SERVICE_NAME,
                "event_type": "change-indicator-tags",
                "object_type": "indicator",
                "object_name": "Indicator",
                "description": "Change tags for indicator",
                "prev_value": prev_indicator_value,
                "new_value": get_indicator_logging_data(
                    Indicator.objects.get(id=indicator_id),
                ),
            })

            return Response(status=status.HTTP_200_OK)

        return Response(
            data={"detail": "Indicator not found"},
            status=status.HTTP_404_NOT_FOUND,
        )


class IndicatorAddComment(APIView):
    """Add comment for the indicator"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Add comment"""

        indicator_id = kwargs.get("indicator_id")
        indicator = get_indicator_or_error_response(indicator_id)

        if isinstance(indicator, Response):
            return indicator

        if not request.data.get("details"):
            return Response(
                {"detail": "Details not specified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        create_indicator_activity({
            "indicator_id": indicator_id,
            "activity_type": "add-comment",
            "created_by": request.user.id,
            "details": request.data.get("details"),
        })

        create_audit_log_entry(request, {
            "table": "Console API | indicator_activities",
            "event_type": "add-comment",
            "object_type": "IndicatorActivities",
            "object_name": "Comment",
            "description": "Add comment",
        })

        return Response(status=status.HTTP_201_CREATED)


class IndicatorIsSendingToDetectionsView(APIView):
    """Change is_sending_to_detections field for the indicator"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Change is_sending_to_detections field"""

        is_sending_to_detections: bool | None = request.data.get(
            "is-sending-to-detections",
        )

        if not is_sending_to_detections:
            return Response(
                {"detail": "No value provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        indicator_id = kwargs.get("indicator_id")
        indicator = get_indicator_or_error_response(indicator_id)

        if isinstance(indicator, Response):
            return indicator

        prev_indicator_value = get_indicator_logging_data(indicator)

        indicator.is_sending_to_detections = is_sending_to_detections
        indicator.save()

        create_indicator_activity({
            "indicator_id": indicator.id,
            "activity_type": "Change is_sending_to_detections field",
            "created_by": request.user.id,
            "details": request.data.get("details"),
        })

        create_audit_log_entry(request, {
            "table": LOG_SERVICE_NAME,
            "event_type": "change-indicator-is-sending-to-detections",
            "object_type": "indicator",
            "object_name": "Indicator",
            "description": "Change is_sending_to_detections field",
            "prev_value": prev_indicator_value,
            "new_value": get_indicator_logging_data(indicator),
        })

        return Response(status=status.HTTP_200_OK)


class ScoreIndicatorsView(APIView):
    """Update feeds now"""

    def post(self, request: Request, *args, **kwargs) -> Response:
        score_service_update_endpoint = f"{settings.SCORE_SERVICE_URL}/api/force-update"

        try:
            requests.get(score_service_update_endpoint)
        except Exception as error:
            return Response({"detail": str(error)}, status=HTTP_400_BAD_REQUEST)

        create_audit_log_entry(request, {
            "table": "data-processing-worker",
            "event_type": "update-indicators",
            "object_type": "indicator",
            "object_name": "Indicator",
            "description": "Score indicator weight",
        })

        return Response(status=HTTP_200_OK)
