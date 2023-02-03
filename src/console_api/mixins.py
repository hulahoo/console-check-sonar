"""Mixins for the project"""

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_400_BAD_REQUEST

from console_api.feed.models import IndicatorFeedRelationship, Feed
from console_api.indicator.models import IndicatorActivities
from console_api.services import get_filter_query_param
from console_api.services import get_sort_by_param


class SortAndFilterQuerysetMixin:
    """Mixin for sorting and filtering a queryset"""

    def get_error_or_sort_and_filter_queryset(self, request, *_, **__):
        """Sort by param and filter the queryset"""

        try:
            self._filter_queryset(request)

            if sort_by := get_sort_by_param(request):
                if sort_by not in self._SORT_BY_PARAMS:
                    return Response(
                        {"detail": "Wrong value for sort-by parameter"},
                        status=HTTP_400_BAD_REQUEST,
                    )

                self.queryset = self.queryset.order_by(sort_by)
        except Exception as error:
            return Response(
                {"detail": str(error)},
                status=HTTP_400_BAD_REQUEST,
            )


class IndicatorQueryMixin:
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
