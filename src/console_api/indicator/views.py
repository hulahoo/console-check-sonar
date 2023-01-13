"""Views for detections app"""

from uuid import UUID

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)

from console_api.services import (
    CustomTokenAuthentication,
    get_filter_query_param,
    get_response_with_pagination,
)
from console_api.indicator.models import Indicator, IndicatorActivities
from console_api.indicator.serializers import (
    IndicatorListSerializer,
    IndicatorDetailSerializer,
    IndicatorSerializer,
)
from console_api.tag.models import IndicatorTagRelationship, Tag
from console_api.feed.models import IndicatorFeedRelationship, Feed


class IndicatorListView(generics.ListAPIView):
    """List of indicators"""

    queryset = Indicator.objects.all()
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

        id_ = get_filter_query_param(request, "id")
        ioc_type = get_filter_query_param(request, "ioc-type")
        value = get_filter_query_param(request, "value")
        context = get_filter_query_param(request, "context")

        first_detected_at = get_filter_query_param(request, "first-detected-at")
        last_detected_at = get_filter_query_param(request, "last-detected-at")

        created_at_from = get_filter_query_param(request, "created-at-from")
        created_at_to = get_filter_query_param(request, "created-at-to")

        created_by = get_filter_query_param(request, "created-by")

        updated_at_from = get_filter_query_param(request, "updated-at-from")
        updated_at_to = get_filter_query_param(request, "updated-at-to")

        if id_:
            self.queryset = self.queryset.filter(id=id_)
        if ioc_type:
            self.queryset = self.queryset.filter(ioc_type=ioc_type)
        if value:
            self.queryset = self.queryset.filter(value=value)
        if context:
            self.queryset = self.queryset.filter(context=context)

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

        if created_by:
            self.queryset = self.queryset.filter(created_by=created_by)

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
    serializer_class = IndicatorSerializer
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


class IndicatorDetailView(generics.RetrieveAPIView):
    """Indicator detail view"""

    serializer_class = IndicatorDetailSerializer
    lookup_field = "id"
    queryset = Indicator.objects.all()
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]


@api_view(("POST",))
@require_http_methods(["POST"])
@renderer_classes((JSONRenderer,))
def change_indicator_tags_view(request: Request, indicator_id: UUID) -> Response:
    """Change tags list for the indicator"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=HTTP_403_FORBIDDEN
        )

    if not request.data.get("tags"):
        return Response(
            {"detail": "Tags not specified"},
            status=HTTP_400_BAD_REQUEST,
        )

    tags = request.data.get("tags")
    tags = tags.replace("[", "").replace("]", "").replace(" ", "").split(",")

    if not all(tag.isdigit() for tag in tags):
        return Response(
            {"detail": "Tags not valid"},
            status=HTTP_400_BAD_REQUEST,
        )

    new_tags = [int(tag) for tag in tags if tag != ""]

    if request.method == "POST":
        if Indicator.objects.filter(id=indicator_id).exists():
            if any(not Tag.objects.filter(id=tag).exists() for tag in new_tags):
                return Response(
                    {"detail": "Tags wrong"},
                    status=HTTP_400_BAD_REQUEST,
                )

            IndicatorTagRelationship.objects.filter(
                indicator_id=indicator_id,
            ).delete()

            for tag in new_tags:
                IndicatorTagRelationship.objects.create(
                    indicator_id=indicator_id,
                    tag_id=tag,
                )

            return Response(status=HTTP_200_OK)

        request.errors = {"detail": "Indicator not found"}

    return Response(request.errors, status=HTTP_400_BAD_REQUEST)


@api_view(("POST",))
@require_http_methods(["POST"])
@renderer_classes((JSONRenderer,))
def add_comment_view(request: Request, indicator_id: UUID) -> Response:
    """Change tags list for the indicator"""

    if not CustomTokenAuthentication().authenticate(request):
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=HTTP_403_FORBIDDEN
        )

    if request.method == "POST":
        if not Indicator.objects.filter(id=indicator_id).exists():
            return Response(
                {"error": "Indicator doesn't exists"},
                status=HTTP_400_BAD_REQUEST,
            )

        if not request.data.get("details"):
            return Response(
                {"error": "Details not specified"},
                status=HTTP_400_BAD_REQUEST,
            )

        activity = IndicatorActivities(
            id=IndicatorActivities.objects.order_by("id").last().id + 1,
            indicator_id=indicator_id,
            activity_type="add-comment",
            details=request.data.get("details"),
            created_by=request.data.get("created-by"),
        )
        activity.save()

        return Response(status=HTTP_201_CREATED)

    return Response(request.errors, status=HTTP_400_BAD_REQUEST)
