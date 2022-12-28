"""Views for detections app"""

from django.http import JsonResponse
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.request import Request

from console_api.api.services import (
    get_filter_query_param,
    get_response_with_pagination,
)
from console_api.apps.indicator.models import Indicator
from console_api.api.indicator.serializers import (
    IndicatorListSerializer, IndicatorDetailSerializer, IndicatorSerializer,
)
from console_api.apps.tag.models import IndicatorTagRelationship
from console_api.apps.feed.models import IndicatorFeedRelationship, Feed


class IndicatorStatiscList(generics.ListAPIView):
    """IndicatorStatiscList"""

    queryset = Indicator.objects.all()
    serializer_class = IndicatorListSerializer

    def add_queryset_filters(self, request: Request) -> None:
        """Filter the queryset"""

        id_ = get_filter_query_param(request, "id")
        ioc_type = get_filter_query_param(request, "ioc-type")
        tags = get_filter_query_param(request, "tags")
        feed_name = get_filter_query_param(request, "feed-name")
        value = get_filter_query_param(request, "value")
        context = get_filter_query_param(request, "context")
        is_sending_to_detections = get_filter_query_param(request, "is-sending-to-detections")
        is_false_positive = get_filter_query_param(request, "is-false-positive")
        weight = get_filter_query_param(request, "weight")
        feeds_weight = get_filter_query_param(request, "feeds-weight")
        tags_weight = get_filter_query_param(request, "tags-weight")
        time_weight = get_filter_query_param(request, "time-weight")
        is_archived = get_filter_query_param(request, "is-archived")
        false_detected_counter = get_filter_query_param(request, "false-detected-counter")
        positive_detected_counter = get_filter_query_param(request, "positive-detected-counter")
        total_detected_counter = get_filter_query_param(request, "total-detected-counter")
        first_detected_at = get_filter_query_param(request, "first-detected-at")
        last_detected_at = get_filter_query_param(request, "last-detected-at")
        created_at = get_filter_query_param(request, "created-at")
        created_by = get_filter_query_param(request, "created-by")
        updated_at = get_filter_query_param(request, "updated-at")

        if id_:
            self.queryset = self.queryset.filter(id=id_)
        if ioc_type:
            self.queryset = self.queryset.filter(ioc_type=ioc_type)
        if value:
            self.queryset = self.queryset.filter(value=value)
        if context:
            self.queryset = self.queryset.filter(context=context)
        if is_sending_to_detections:
            self.queryset = self.queryset.filter(is_sending_to_detections=is_sending_to_detections)
        if is_false_positive:
            self.queryset = self.queryset.filter(is_false_positive=is_false_positive)
        if weight:
            self.queryset = self.queryset.filter(weight=weight)
        if feeds_weight:
            self.queryset = self.queryset.filter(feeds_weight=feeds_weight)
        if tags_weight:
            self.queryset = self.queryset.filter(tags_weight=tags_weight)
        if time_weight:
            self.queryset = self.queryset.filter(time_weight=time_weight)
        if is_archived:
            self.queryset = self.queryset.filter(is_archived=is_archived)
        if false_detected_counter:
            self.queryset = self.queryset.filter(false_detected_counter=false_detected_counter)
        if positive_detected_counter:
            self.queryset = self.queryset.filter(positive_detected_counter=positive_detected_counter)
        if total_detected_counter:
            self.queryset = self.queryset.filter(total_detected_counter=total_detected_counter)
        if first_detected_at:
            self.queryset = self.queryset.filter(first_detected_at=first_detected_at)
        if last_detected_at:
            self.queryset = self.queryset.filter(last_detected_at=last_detected_at)
        if created_at:
            self.queryset = self.queryset.filter(created_at=created_at)
        if created_by:
            self.queryset = self.queryset.filter(created_by=created_by)
        if updated_at:
            self.queryset = self.queryset.filter(updated_at=updated_at)

        # tags and feed_name should be below others
        if tags:
            tags = tags.replace(' ', '').replace('[', '').replace(']', '')
            tags = tags.split(',')

            if tags == ['']:
                tags = []

            tags = [int(number) for number in tags]

            tags_filtered_list = []

            for indicator in self.queryset:
                indicator_tags = [
                    relationship.tag_id for relationship in
                    IndicatorTagRelationship.objects.filter(
                        indicator_id=indicator.id,
                    )
                ]

                if tags == []:
                    if indicator_tags == []:
                        tags_filtered_list.append(indicator)
                else:
                    if set(tags).issubset(set(indicator_tags)):
                        tags_filtered_list.append(indicator)

            self.queryset = tags_filtered_list
        if feed_name and feed_name != '':
            feed_filtered_list = []

            for indicator in self.queryset:
                feeds = [
                    Feed.objects.get(id=relationship.feed_id).title
                    for relationship in
                    IndicatorFeedRelationship.objects.filter(
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

        if sort_by_param := request.GET.get('sort-by'):
            sort_by_param = \
                sort_by_param[0] + sort_by_param[1:].replace('-', '_')

            if sort_by_param in ['ioc_weight', '-ioc_weight']:
                sort_by_param = 'weight'

            self.queryset = self.queryset.order_by(sort_by_param)

        return get_response_with_pagination(
            request, self.queryset, self.get_serializer,
        )


class IndicatorCreateView(viewsets.ModelViewSet):
    """IndicatorCreateView"""

    authentication_classes = ()
    permission_classes = []
    serializer_class = IndicatorSerializer
    queryset = Indicator.objects.all()

    def create(self, request, *args, **kwargs):
        super(IndicatorCreateView, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        super(IndicatorCreateView, self).update(request, *args, **kwargs)

    def get(self, request, * args, **kwargs):
        start_period = request.GET.get('start-period-at')
        finish_period = request.GET.get('finish-period-at')
        self.param_dict = {'start_period': start_period, 'finish_period': finish_period}
        return self.list(request, *args, **kwargs)


class IndicatorView(generics.ListAPIView):
    """
    (GET) Получение списка индикаторов
    """

    serializer_class = IndicatorListSerializer
    queryset = Indicator.objects.all()


class IndicatorDetailView(generics.RetrieveAPIView):
    """Indicator detail view"""

    serializer_class = IndicatorDetailSerializer
    lookup_field = 'id'
    queryset = Indicator.objects.all()
