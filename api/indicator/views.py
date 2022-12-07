from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination

from src.indicator.models import Indicator
from api.indicator.filters import IndicatorFilter, DashboardFilter
from api.indicator.serializers import IndicatorSerializer, IndicatorWithFeedsSerializer


class IndicatorListView(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IndicatorFilter


class Dashboard(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = IndicatorWithFeedsSerializer
    queryset = Indicator.objects.all().prefetch_related('feeds')
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DashboardFilter
