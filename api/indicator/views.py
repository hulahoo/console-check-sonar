import collections

from django.db import connection
from django.db.models import Count, Sum
from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.indicator.filters import DashboardFilter, IndicatorFilter
from api.indicator.serializers import (DataIndicatorSerializer,
                                       IndicatorWithFeedsSerializer,
                                       MatchedIndicatorSerializer, IndicatorSerializer)
from src.feed.models import Feed
from src.indicator.models import Indicator
from src.source.models import Source


class IndicatorStatiscList(generics.ListAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({"data": serializer.data})

    def get_queryset(self):
        return (Indicator.objects
                .values('type', 'detected')
                .annotate(checked_count=Count('type'), detected_count=Sum('detected'))
                .order_by('type'))


class FeedStatiscList(generics.ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = IndicatorWithFeedsSerializer
    queryset = Indicator.objects.all().prefetch_related('feeds')


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
    serializer_class = MatchedIndicatorSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return JsonResponse({"data": queryset})

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
            sources_ind: dict = collections.defaultdict(list)
            intersect_weight: dict = collections.defaultdict(dict)
            for item in data:
                indicators = [i for i in data if i['source_id'] == item['source_id']]
                sum_ind = collections.Counter(item["indicator_id"] for item in indicators)
                sources_ind[item.get('source_name')] = dict(sum_ind)

        for source, _ in sorted(sources_ind.items()):
            new_sources_ind = list(sources_ind.keys())
            new_sources_ind.remove(source)
            a = set(sources_ind.get(source).keys())
            for src in new_sources_ind:
                b = set(sources_ind.get(src).keys())
                c = a.intersection(b)
                intersect_weight[source].update({src: len(c) / len(a) * 100})
        return intersect_weight
