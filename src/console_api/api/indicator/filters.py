import django_filters
from django_filters import rest_framework as filters

from console_api.apps.indicator.models import Indicator


class DashboardFilter(filters.FilterSet):
    name = django_filters.CharFilter(field_name='feeds__name', lookup_expr='iexact')
    ts = django_filters.DateTimeFilter(field_name='feeds__ts', lookup_expr='iexact')

    class Meta:
        model = Indicator
        fields = ["id", "positive_detected_counter", "false_detected_counter"]


class IndicatorFilter(filters.FilterSet):

    class Meta:
        model = Indicator
        fields = ["type", "detected"]
