"""Views for detections app"""

from datetime import datetime

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from console_api.services import (
    CustomTokenAuthentication,
    get_filter_query_param,
    get_response_with_pagination,
)
from console_api.indicator.models import Indicator, IndicatorActivities
from console_api.indicator.serializers import (
    IndicatorCreateSerializer,
    IndicatorDetailSerializer,
    IndicatorListSerializer,
)
from console_api.tag.models import IndicatorTagRelationship, Tag
from console_api.feed.models import IndicatorFeedRelationship, Feed


class IndicatorListView(generics.ListAPIView):
    """List of indicators"""

    queryset = Indicator.objects.filter(deleted_at=None)
    serializer_class = IndicatorListSerializer

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def add_counter_queryset_filters(self, request: Request) -> None:
        """Filter the queryset"""

        false_detected_counter = get_filter_query_param(
            request, "false-detected-counter"
        )
        positive_detected_counter = get_filter_query_param(
            request, "positive-detected-counter"
        )
        total_detected_counter = get_filter_query_param(
            request, "total-detected-counter"
        )

        if false_detected_counter:
            self.queryset = self.queryset.filter(
                false_detected_counter=false_detected_counter
            )
        if positive_detected_counter:
            self.queryset = self.queryset.filter(
                positive_detected_counter=positive_detected_counter
            )
        if total_detected_counter:
            self.queryset = self.queryset.filter(
                total_detected_counter=total_detected_counter
            )

    def add_boolean_filters(self, request: Request) -> None:
        """Filter the queryset"""

        is_sending_to_detections = get_filter_query_param(
            request, "is-sending-to-detections"
        )
        is_false_positive = get_filter_query_param(request, "is-false-positive")
        is_archived = get_filter_query_param(request, "is-archived")

        if is_sending_to_detections:
            self.queryset = self.queryset.filter(
                is_sending_to_detections=is_sending_to_detections
            )
        if is_false_positive:
            self.queryset = self.queryset.filter(is_false_positive=is_false_positive)
        if is_archived:
            self.queryset = self.queryset.filter(is_archived=is_archived)

    def add_weight_filters(self, request: Request) -> None:
        """Filter the queryset"""

        weight_from = get_filter_query_param(request, "weight-from")
        weight_to = get_filter_query_param(request, "weight-to")

        feeds_weight = get_filter_query_param(request, "feeds-weight")

        tags_weight_from = get_filter_query_param(request, "tags-weight-from")
        tags_weight_to = get_filter_query_param(request, "tags-weight-to")

        time_weight = get_filter_query_param(request, "time-weight")

        if weight_from or weight_to:
            if not weight_from:
                weight_from = 0

            if not weight_to:
                weight_to = 100

            self.queryset = self.queryset.filter(
                weight__range=(weight_from, weight_to),
            )

        if tags_weight_from or tags_weight_to:
            if not tags_weight_from:
                tags_weight_from = 0

            if not tags_weight_to:
                tags_weight_to = 100

            self.queryset = self.queryset.filter(
                tags_weight__range=(tags_weight_from, tags_weight_to),
            )

        if feeds_weight:
            self.queryset = self.queryset.filter(feeds_weight=feeds_weight)
        if time_weight:
            self.queryset = self.queryset.filter(time_weight=time_weight)

    def add_queryset_filters(self, request: Request) -> None:
        """Filter the queryset"""

        indicator_id = get_filter_query_param(request, "indicator-id")
        ioc_type = get_filter_query_param(request, "ioc-type")
        value = get_filter_query_param(request, "value")
        context = get_filter_query_param(request, "context")

        created_by = get_filter_query_param(request, "created-by")

        comment = get_filter_query_param(request, "comment")

        if indicator_id:
            self.queryset = self.queryset.filter(id=indicator_id)
        if ioc_type:
            self.queryset = self.queryset.filter(ioc_type=ioc_type)
        if value:
            self.queryset = self.queryset.filter(value=value)
        if context:
            self.queryset = self.queryset.filter(context=context)

        if created_by:
            self.queryset = self.queryset.filter(created_by=created_by)

        if comment:
            self.queryset = self.queryset.filter(
                id__in=IndicatorActivities.objects.values("indicator_id").filter(details__icontains=comment)
            )

    def add_queryset_at_time_filters(self, request: Request) -> None:
        """Filter the queryset"""

        first_detected_at = get_filter_query_param(request, "first-detected-at")
        last_detected_at = get_filter_query_param(request, "last-detected-at")

        created_at_from = get_filter_query_param(request, "created-at-from")
        created_at_to = get_filter_query_param(request, "created-at-to")

        updated_at_from = get_filter_query_param(request, "updated-at-from")
        updated_at_to = get_filter_query_param(request, "updated-at-to")

        if updated_at_from and updated_at_to:
            self.queryset = self.queryset.filter(
                updated_at__range=(updated_at_from, updated_at_to),
            )
        elif updated_at_from:
            self.queryset = self.queryset.filter(
                updated_at__gte=updated_at_from,
            )
        elif updated_at_to:
            self.queryset = self.queryset.filter(
                updated_at__lte=updated_at_to,
            )

        if first_detected_at:
            self.queryset = self.queryset.filter(first_detected_at=first_detected_at)
        if last_detected_at:
            self.queryset = self.queryset.filter(last_detected_at=last_detected_at)

        if created_at_from and created_at_to:
            self.queryset = self.queryset.filter(
                created_at__range=(created_at_from, created_at_to),
            )
        elif created_at_from:
            self.queryset = self.queryset.filter(
                created_at__gte=created_at_from,
            )
        elif created_at_to:
            self.queryset = self.queryset.filter(
                created_at__lte=created_at_to,
            )

    # Потом раскомментить и пофиксить
    def add_tags_filters(self, request: Request) -> None:
        """Filter the queryset"""

        pass

    def add_feed_name_filters(self, request: Request) -> None:
        """Filter the queryset"""

        feed_name = get_filter_query_param(request, "feed-name")

        if feed_name and feed_name != "":
            feed_filtered_list = []

            for indicator in self.queryset:
                feeds = [
                    Feed.objects.get(id=relationship.feed_id).title
                    for relationship in IndicatorFeedRelationship.objects.filter(
                        indicator_id=indicator.id,
                    )
                ]

                if feed_name in feeds:
                    feed_filtered_list.append(indicator)

            self.queryset = feed_filtered_list

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


class IndicatorCreateView(viewsets.ModelViewSet):
    """IndicatorCreateView"""

    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = IndicatorCreateSerializer
    queryset = Indicator.objects.all()

    def create(self, request, *args, **kwargs):
        super(IndicatorCreateView, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        super(IndicatorCreateView, self).update(request, *args, **kwargs)

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


class ChangeIndicatorTags(APIView):
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

        activity = IndicatorActivities(
            id=IndicatorActivities.objects.order_by("id").last().id + 1,
            indicator_id=indicator_id,
            activity_type="add-comment",
            details=request.data.get("details"),
            created_by=request.data.get("created-by"),
        )
        activity.save()

        return Response(status=status.HTTP_201_CREATED)
