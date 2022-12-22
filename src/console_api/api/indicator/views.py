"""Views for detections app"""
from rest_framework import generics, viewsets

from console_api.apps.indicator.models import Indicator
from console_api.api.services import get_response_with_pagination
from console_api.api.indicator.serializers import (
    IndicatorListSerializer, IndicatorDetailSerializer, IndicatorSerializer,
)


class IndicatorStatiscList(generics.ListAPIView):
    """IndicatorStatiscList"""

    def add_queryset_filters(self, *, request):
        is_sending_to_detections = request.GET.get('filter[is_sending_to_detections]')
        is_false_positive = request.GET.get('filter[is_false_positive]')
        weight = request.GET.get('filter[weight]')
        tags_weight = request.GET.get('filter[tags_weight]')
        is_archived = request.GET.get('filter[is_archived]')
        false_detected_counter = request.GET.get('filter[false_detected_counter]')
        positive_detected_counter = request.GET.get('filter[positive_detected_counter]')
        total_detected_counter = request.GET.get('filter[total_detected_counter]')
        first_detected_at = request.GET.get('filter[first_detected_at]')
        last_detected_at = request.GET.get('filter[last_detected_at]')

        if request.GET.get('filter[id]'):
            self.queryset = self.queryset.filter(id=request.GET.get('filter[id]'))
        if request.GET.get('filter[ioc-type]'):
            self.queryset = self.queryset.filter(ioc_type=request.GET.get('filter[ioc-type]'))
        if request.GET.get('filter[value]'):
            self.queryset = self.queryset.filter(value=request.GET.get('filter[value]'))
        if is_sending_to_detections:
            self.queryset = self.queryset.filter(is_sending_to_detections=is_sending_to_detections)
        if is_false_positive:
            self.queryset = self.queryset.filter(is_false_positive=is_false_positive)
        if weight:
            self.queryset = self.queryset.filter(weight=weight)
        if tags_weight:
            self.queryset = self.queryset.filter(tags_weight=tags_weight)
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

    def list(self, request, *args, **kwargs):
        sort_by_param = request.GET.get('sort-by')
        self.queryset = self.add_queryset_filters(request=request)

        if sort_by_param:
            sort_by_param = \
                sort_by_param[0] + sort_by_param[1:].replace('-', '_')

            if sort_by_param in ['ioc_weight', '-ioc_weight']:
                sort_by_param = 'weight'

            self.queryset = self.queryset.order_by(sort_by_param)

        return get_response_with_pagination(
            request, self.queryset, self.get_serializer,
        )

    serializer_class = IndicatorListSerializer
    queryset = Indicator.objects.all()


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
    """
    (GET) Деталка сотрудника
    """

    serializer_class = IndicatorDetailSerializer
    lookup_field = 'id'
    queryset = Indicator.objects.all()
