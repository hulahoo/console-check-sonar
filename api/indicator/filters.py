from django_filters import rest_framework as filters

from src.indicator.models import Indicator


class IndicatorFilter(filters.FilterSet):
    class Meta:
        model = Indicator
        fields = Indicator.get_model_fields()
