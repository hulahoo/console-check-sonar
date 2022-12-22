from rest_framework import generics
from django.db.models import Count

from console_api.apps.indicator.models import Indicator


class BaseIndicatorList(generics.ListAPIView):
    queryset = Indicator.objects.all()
    pagination_class = None
    serializer_class = None

    def get_queryset(self):
        start_period = self.param_dict.get('start_period')
        finish_period = self.param_dict.get('finish_period')
        return (Indicator.objects
                .values('value')
                .filter(last_detected_date__range=(start_period, finish_period))
                .annotate(detected_count=Count('detected'))
                .order_by('last_detected_date'))

    def get(self, request, * args, **kwargs):
        start_period = request.GET.get('start-period-at')
        finish_period = request.GET.get('finish-period-at')
        self.param_dict = {'start_period': start_period, 'finish_period': finish_period}
        return self.list(request, *args, **kwargs)
