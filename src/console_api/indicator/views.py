"""Views for detections app"""

from datetime import datetime

from rest_framework import status
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from console_api.mixins import IndicatorQueryMixin
from console_api.config.logger_config import logger
from console_api.services import CustomTokenAuthentication
from console_api.services import get_response_with_pagination
from console_api.tag.models import Tag, IndicatorTagRelationship
from console_api.indicator.models import Indicator, IndicatorActivities
from console_api.indicator.serializers import (
    IndicatorCreateSerializer,
    IndicatorDetailSerializer,
    IndicatorListSerializer,
)


def create_indicator_activity(data: dict) -> None:
    """Create IndicatorActivities object"""

    activity = IndicatorActivities(
        id=IndicatorActivities.objects.order_by("id").last().id + 1,
        indicator_id=data.get("indicator_id"),
        activity_type=data.get("activity_type"),
        created_by=data.get("created_by"),
        details=data.get("details"),
    )
    activity.save()

    logger.info(f"Created indicator activity: {activity.id}")


class IndicatorView(viewsets.ModelViewSet, IndicatorQueryMixin):
    """List of indicators"""

    queryset = Indicator.objects.filter(deleted_at=None)
    serializer_classes = {
        "list": IndicatorListSerializer,
        "create": IndicatorCreateSerializer
    }

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request: Request) -> Response:
        """Return response with list of indicators"""

        self.queryset = self.get_queryset()

        if not self.queryset:
            return JsonResponse({"data": []})

        self.add_queryset_filters(request=request)
        self.add_counter_queryset_filters(request=request)
        self.add_boolean_filters(request=request)
        self.add_weight_filters(request=request)
        self.add_queryset_at_time_filters(request=request)

        # tags and feed_name should be below others
        # self.add_tags_filters(request=request)
        self.add_feed_name_filters(request=request)

        if sort_by_param := request.GET.get("sort-by"):
            sort_by_param = sort_by_param[0] + sort_by_param[1:].replace("-", "_")

            if sort_by_param in ["ioc_weight", "-ioc_weight"]:
                sort_by_param = "weight"

            self.queryset = self.queryset.order_by(sort_by_param)

        return get_response_with_pagination(
            request,
            self.queryset,
            self.get_serializer,
        )

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def create(self, request: Request, *args, **kwargs):
        if not request.data:
            return Response(
                {"detail": "Missing fields"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            status=status.HTTP_201_CREATED,
            data={"data": "Indicator created successfully"}
        )

    def get(self, request, *args, **kwargs):
        start_period = request.GET.get("start-period-at")
        finish_period = request.GET.get("finish-period-at")
        self.param_dict = {"start_period": start_period, "finish_period": finish_period}
        return self.list(request, *args, **kwargs)


class MarkIndicatorAsFalsePositiveView(APIView):
    """Mark the indicator as false positive"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, *args, **kwargs) -> Response:
        indicator_id = kwargs.get("indicator_id")

        if not Indicator.objects.filter(id=indicator_id).exists():
            return Response(
                {"detail": f"Indicator with id {indicator_id} doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        indicator = Indicator.objects.get(id=indicator_id)
        indicator.is_false_positive = True
        indicator.save()

        create_indicator_activity({
            "indicator_id": indicator_id,
            "activity_type": "mark-as-false-positive",
            "created_by": request.user.id,
            "details": request.data.get("details"),
        })

        return Response(status=status.HTTP_200_OK)


class IndicatorDetail(APIView):

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_indicator_detail(self, *, indicator_id) -> Indicator:
        if not Indicator.objects.filter(id=indicator_id).exists():
            return Response(
                {"detail": f"Indicator with id {indicator_id} doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Indicator.objects.get(id=indicator_id)

    def get(self, request: Request, *args, **kwargs) -> Response:
        indicator = self.get_indicator_detail(indicator_id=kwargs.get("indicator_id"))
        serialized_data = IndicatorDetailSerializer(instance=indicator).data
        return Response(
            data=serialized_data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request: Request, *args, **kwargs) -> Response:
        indicator = self.get_indicator_detail(indicator_id=kwargs.get("indicator_id"))
        indicator.deleted_at = datetime.now()
        indicator.save()

        return Response(status=status.HTTP_200_OK)


class ChangeIndicatorTagsView(APIView):
    """Change tags for the indicator"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        indicator_id = kwargs.get("indicator_id")
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

        if Indicator.objects.filter(id=indicator_id).exists():
            if any(not Tag.objects.filter(id=tag).exists() for tag in new_tags):
                return Response(
                    {"detail": "Tags wrong"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            IndicatorTagRelationship.objects.filter(
                indicator_id=indicator_id,
            ).delete()

            for tag in new_tags:
                IndicatorTagRelationship.objects.create(
                    indicator_id=indicator_id,
                    tag_id=tag,
                )

            create_indicator_activity({
                "indicator_id": indicator_id,
                "activity_type": "update-tags",
                "created_by": request.user.id,
                "details": request.data.get("details"),
            })

            return Response(status=status.HTTP_200_OK)

        return Response(
            data={"detail": "Indicator not found"},
            status=status.HTTP_404_NOT_FOUND,
        )


class IndicatorAddComment(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Change tags list for the indicator"""
        indicator_id = kwargs.get("indicator_id")

        if not Indicator.objects.filter(id=indicator_id).exists():
            return Response(
                {"error": "Indicator doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not request.data.get("details"):
            return Response(
                {"error": "Details not specified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        create_indicator_activity({
            "indicator_id": indicator_id,
            "activity_type": "Change is_sending_to_detections field",
            "created_by": request.user.id,
            "details": request.data.get("details"),
        })

        return Response(status=status.HTTP_201_CREATED)


class IndicatorIsSendingToDetectionsView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        value: bool = request.data.get("value")
        if not value:
            return Response(
                {"error": "No value provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        indicator_id = kwargs.get("indicator_id")
        if not Indicator.objects.filter(id=indicator_id).exists():
            return Response(
                {"error": "Indicator doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        indicator = Indicator.objects.get(id=indicator_id)
        indicator.is_sending_to_detections = value
        indicator.save()

        create_indicator_activity({
            "indicator_id": indicator.id,
            "activity_type": "Change is_sending_to_detections field",
            "created_by": request.user.id,
            "details": request.data.get("details"),
        })

        return Response(
            data={"data": "is_sending_to_detections changed"},
            status=status.HTTP_200_OK,
        )
