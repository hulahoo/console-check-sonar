from rest_framework import viewsets, generics
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Sum
from django.http import HttpRequest

from src.indicator.models import Indicator
from src.feed.models import Feed
from api.indicator.filters import IndicatorFilter, DashboardFilter
from api.indicator.serializers import IndicatorSerializer, IndicatorWithFeedsSerializer, MatchedIndicatorSerializer


class IndicatorStatiscList(generics.ListAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer

    def get_queryset(self):
        return (Indicator.objects
                .values('type', 'detected')
                .annotate(checked_count=Count('type'), detected_count=Sum('detected'))
                .order_by('type'))
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = IndicatorFilter


class FeedStatiscList(generics.ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = IndicatorWithFeedsSerializer
    queryset = Indicator.objects.all().prefetch_related('feeds')
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = DashboardFilter


class MatchedIndicatorStatiscList(generics.ListAPIView):
    queryset = Indicator.objects.all()
    serializer_class = MatchedIndicatorSerializer

    def get_queryset(self):
        start_period = self.param_dict.get('start_period')
        finish_period = self.param_dict.get('finish_period')
        return (Indicator.objects
                .values('last_detected_date')
                .filter(last_detected_date__range=(start_period, finish_period))
                .annotate(detected_count=Sum('detected'))
                .order_by('last_detected_date'))

    def get(self, request, * args, **kwargs):
        start_period = request.GET.get('start-period-at')
        finish_period = request.GET.get('finish-period-at')
        self.param_dict = {'start_period': start_period, 'finish_period': finish_period}
        return self.list(request, *args, **kwargs)


class MatchedObjectsStatiscList(generics.ListAPIView):
    queryset = Indicator.objects.all()
    serializer_class = MatchedIndicatorSerializer

    def get_queryset(self):
        start_period = self.param_dict.get('start_period')
        finish_period = self.param_dict.get('finish_period')
        return (Indicator.objects
                .values('last_detected_date')
                .filter(last_detected_date__range=(start_period, finish_period))
                .annotate(detected_count=Sum('detected'))
                .order_by('last_detected_date'))

    def get(self, request, * args, **kwargs):
        start_period = request.GET.get('start-period-at')
        finish_period = request.GET.get('finish-period-at')
        self.param_dict = {'start_period': start_period, 'finish_period': finish_period}
        return self.list(request, *args, **kwargs)


class CheckedObjectsStatiscList(generics.ListAPIView):
    queryset = Indicator.objects.all()
    serializer_class = MatchedIndicatorSerializer

    def get_queryset(self):
        start_period = self.param_dict.get('start_period')
        finish_period = self.param_dict.get('finish_period')
        return (Indicator.objects
                .values('last_detected_date')
                .filter(last_detected_date__range=(start_period, finish_period))
                .annotate(detected_count=Count('detected'))
                .order_by('last_detected_date'))

    def get(self, request, * args, **kwargs):
        start_period = request.GET.get('start-period-at')
        finish_period = request.GET.get('finish-period-at')
        self.param_dict = {'start_period': start_period, 'finish_period': finish_period}
        return self.list(request, *args, **kwargs)


class FeedsIntersectionList(generics.ListAPIView):
    queryset = Feed.objects.all()
    serializer_class = MatchedIndicatorSerializer

    def get_queryset(self):
        return (Indicator.objects
                .values('last_detected_date')
                .filter()
                .annotate(detected_count=Count('detected'))
                .order_by('last_detected_date'))
