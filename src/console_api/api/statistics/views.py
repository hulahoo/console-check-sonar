import collections

from django.db import connection
from django.db.models import Count, Sum
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from apps.feed.models import Feed
from api.statistics.base import BaseIndicatorList
from apps.indicator.models import Indicator
from apps.source.models import Source
from api.statistics.serializers import (IndicatorSerializer,
                                        IndicatorWithFeedsSerializer,
                                        MatchedIndicatorSerializer)


class IndicatorStatiscList(BaseIndicatorList):
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
    serializer_class = MatchedIndicatorSerializer


class MatchedObjectsStatiscList(generics.ListAPIView):
    serializer_class = MatchedIndicatorSerializer


class CheckedObjectsStatiscList(generics.ListAPIView):
    serializer_class = MatchedIndicatorSerializer


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
                    "left join feeds_indicators as fi on f.id=fi.feed_id" % (Source.objects.model._meta.db_table,
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
            unique_source_ind = set(sources_ind.get(source).keys())
            for src in new_sources_ind:
                unique_source_keys = set(sources_ind.get(src).keys())
                intersection_of_source_inds = unique_source_ind.intersection(unique_source_keys)
                intersect_weight[source].update({src: len(intersection_of_source_inds) / len(unique_source_ind) * 100})
        return intersect_weight
