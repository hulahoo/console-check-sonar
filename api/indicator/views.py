import collections

from django.db import connection
from django.db.models import Count, Sum
from django_filters import rest_framework as filters
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination

from api.indicator.filters import DashboardFilter, IndicatorFilter
from api.indicator.serializers import (IndicatorSerializer,
                                       IndicatorWithFeedsSerializer,
                                       MatchedIndicatorSerializer)
from src.indicator.models import Indicator
from src.source.models import Source
from src.feed.models import Feed


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
    # filter_backends = (filters.DjangoFilterBackend,)import collections
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
    # queryset = Source.objects.prefetch_related('feeds')
    # serializer_class = MatchedIndicatorSerializer

    def get_queryset(self):
        with connection.cursor() as cursor:
            query = "select s.name as source_name, " \
                    "s.id as source_id, " \
                    "fi.indicator_id " \
                    "from %s as s " \
                    "left join %s as f on s.id=f.source_id " \
                    "left join feed_feed_indicators as fi on f.id=fi.feed_id" % (Source.objects.model._meta.db_table,
                                                                                 Feed.objects.model._meta.db_table)
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            data = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
            for item in data:
                indicators = [i for i in data if i['source_id'] == item['source_id']]
                sum_ind = collections.Counter(item["indicator_id"] for item in indicators)

        return 

    def get(self, request, * args, **kwargs):
        sources = self.get_queryset()
        res: dict = collections.defaultdict(list)
        for source in sources:
            new_sources = sources.copy()
            new_sources.pop(source)
            for new_source in new_sources:
                list1 = set(source.feeds)
                list2 = set(new_source.feeds)
                inter = list1 & list2 
                data = len(inter) / len(source) * 100
                res[source.name] = data

        return 
