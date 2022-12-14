from django.db.models import Count, Sum
from django.http import JsonResponse
from rest_framework import generics

from api.indicator.serializers import IndicatorSerializer

from apps.indicator.models import Indicator


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
