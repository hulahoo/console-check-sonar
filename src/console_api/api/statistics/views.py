"""Views for statistics app"""

from django.db.models import Count, Sum
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from console_api.apps.feed.models import Feed
from console_api.api.statistics.base import BaseIndicatorList
from console_api.apps.indicator.models import Indicator
from console_api.api.statistics.serializers import (
    IndicatorSerializer, IndicatorWithFeedsSerializer,
    MatchedIndicatorSerializer,
)


class IndicatorStatiscList(BaseIndicatorList):
    """IndicatorStatiscList"""

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
    """FeedStatiscList"""

    pagination_class = PageNumberPagination
    serializer_class = IndicatorWithFeedsSerializer
    queryset = Indicator.objects.all().prefetch_related('feeds')


class MatchedIndicatorStatiscList(generics.ListAPIView):
    """MatchedIndicatorStatiscList"""

    serializer_class = MatchedIndicatorSerializer
    queryset = Indicator.objects.all().prefetch_related('feeds')


class MatchedObjectsStatiscList(generics.ListAPIView):
    """MatchedObjectsStatiscList"""

    serializer_class = MatchedIndicatorSerializer
    queryset = Indicator.objects.all().prefetch_related('feeds')


class CheckedObjectsStatiscList(generics.ListAPIView):
    """CheckedObjectsStatiscList"""

    serializer_class = MatchedIndicatorSerializer
    queryset = Indicator.objects.all().prefetch_related('feeds')


class FeedsIntersectionList(generics.ListAPIView):
    """FeedsIntersectionList"""

    serializer_class = MatchedIndicatorSerializer
    model = Feed

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return JsonResponse({"data": queryset})
