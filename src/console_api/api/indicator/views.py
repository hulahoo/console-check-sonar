from django.db.models import Count, Sum
from django.http import JsonResponse
from rest_framework import generics, viewsets

from apps.indicator.models import Indicator
from api.indicator.serializers import IndicatorSerializer
from apps.source.models import Source
from django.db import connection
from django.db.models import Count, Sum
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from api.indicator.serializers import IndicatorListSerializer, IndicatorDetailSerializer

"""Views for detections app"""


from apps.indicator.models import Indicator
from api.indicator.serializers import IndicatorSerializer
from api.indicator.services import get_response_with_pagination


class IndicatorStatiscList(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        sort_by_param = request.GET.get('sort-by')

        id_ = request.GET.get('filter[id]')
        ioc_type = request.GET.get('filter[ioc-type]')
        value = request.GET.get('filter[value]')
        is_sending_to_detections = request.GET.get('filter[is_sending_to_detections]')
        is_false_positive = request.GET.get('filter[is_false_positive]')
        weight = request.GET.get('filter[weight]')
        tags_weight = request.GET.get('filter[tags_weight]')
        is_archived = request.GET.get('filter[is_archived]')
        false_detected_counter = request.GET.get('filter[false_detected_counter]')
        positive_detected_counter = request.GET.get('filter[positive_detected_counter]')
        total_detected_counter = request.GET.get('filter[total_detected_counter]')
        first_detected_at = request.GET.get('filter[first_detected_at]')
        last_detected_at = request.GET.get('filter[last_detected_at]')

        if id_:
            self.queryset = self.queryset.filter(id=id_)
        if ioc_type:
            self.queryset = self.queryset.filter(ioc_type=ioc_type)
        if value:
            self.queryset = self.queryset.filter(value=value)
        if is_sending_to_detections:
            self.queryset = self.queryset.filter(is_sending_to_detections=is_sending_to_detections)
        if is_false_positive:
            self.queryset = self.queryset.filter(is_false_positive=is_false_positive)
        if weight:
            self.queryset = self.queryset.filter(weight=weight)
        if tags_weight:
            self.queryset = self.queryset.filter(tags_weight=tags_weight)
        if is_archived:
            self.queryset = self.queryset.filter(is_archived=is_archived)
        if false_detected_counter:
            self.queryset = self.queryset.filter(false_detected_counter=false_detected_counter)
        if positive_detected_counter:
            self.queryset = self.queryset.filter(positive_detected_counter=positive_detected_counter)
        if total_detected_counter:
            self.queryset = self.queryset.filter(total_detected_counter=total_detected_counter)
        if first_detected_at:
            self.queryset = self.queryset.filter(first_detected_at=first_detected_at)
        if last_detected_at:
            self.queryset = self.queryset.filter(last_detected_at=last_detected_at)


        if sort_by_param:
            print(sort_by_param)
            sort_by_param = sort_by_param[0] + sort_by_param[1:].replace('-', '_')
            if sort_by_param == 'ioc_weight' or sort_by_param == '-ioc_weight':
                sort_by_param = 'weight'

            self.queryset = self.queryset.order_by(sort_by_param)

        return get_response_with_pagination(
            request, self.queryset, self.get_serializer,
        )

    serializer_class = IndicatorListSerializer
    queryset = Indicator.objects.all()


class IndicatorCreateView(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = []
    serializer_class = IndicatorSerializer
    queryset = Indicator.objects.all()

    def create(self, request, *args, **kwargs):
        super(IndicatorCreateView, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        super(IndicatorCreateView, self).update(request, *args, **kwargs)

    def get(self, request, * args, **kwargs):
        start_period = request.GET.get('start-period-at')
        finish_period = request.GET.get('finish-period-at')
        self.param_dict = {'start_period': start_period, 'finish_period': finish_period}
        return self.list(request, *args, **kwargs)


# class MatchedObjectsStatiscList(generics.ListAPIView):
#     queryset = Indicator.objects.all()
#     serializer_class = MatchedIndicatorSerializer

#     def get_queryset(self):
#         start_period = self.param_dict.get('start_period')
#         finish_period = self.param_dict.get('finish_period')
#         return (Indicator.objects
#                 .values('last_detected_date')
#                 .filter(last_detected_date__range=(start_period, finish_period))
#                 .annotate(detected_count=Sum('detected'))
#                 .order_by('last_detected_date'))

#     def get(self, request, * args, **kwargs):
#         start_period = request.GET.get('start-period-at')
#         finish_period = request.GET.get('finish-period-at')
#         self.param_dict = {'start_period': start_period, 'finish_period': finish_period}
#         return self.list(request, *args, **kwargs)


# class CheckedObjectsStatiscList(generics.ListAPIView):
#     queryset = Indicator.objects.all()
#     serializer_class = MatchedIndicatorSerializer

#     def get_queryset(self):
#         start_period = self.param_dict.get('start_period')
#         finish_period = self.param_dict.get('finish_period')
#         return (Indicator.objects
#                 .values('last_detected_date')
#                 .filter(last_detected_date__range=(start_period, finish_period))
#                 .annotate(detected_count=Count('detected'))
#                 .order_by('last_detected_date'))

#     def get(self, request, * args, **kwargs):
#         start_period = request.GET.get('start-period-at')
#         finish_period = request.GET.get('finish-period-at')
#         self.param_dict = {'start_period': start_period, 'finish_period': finish_period}
#         return self.list(request, *args, **kwargs)


# class FeedsIntersectionList(generics.ListAPIView):
#     # serializer_class = MatchedIndicatorSerializer

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         return JsonResponse({"data": queryset})

#     def get_queryset(self):
#         with connection.cursor() as cursor:
#             query = "select s.name as source_name, " \
#                     "s.id as source_id, " \
#                     "fi.indicator_id " \
#                     "from %s as s " \
#                     "left join %s as f on s.id=f.source_id " \
#                     "left join feeds_indicators as fi on f.id=fi.feed_id" % (Source.objects.model._meta.db_table,
#                                                                              Feed.objects.model._meta.db_table)
#             cursor.execute(query)
#             columns = [col[0] for col in cursor.description]
#             data = [
#                 dict(zip(columns, row))
#                 for row in cursor.fetchall()
#             ]
#             sources_ind: dict = collections.defaultdict(list)
#             intersect_weight: dict = collections.defaultdict(dict)
#             for item in data:
#                 indicators = [i for i in data if i['source_id'] == item['source_id']]
#                 sum_ind = collections.Counter(item["indicator_id"] for item in indicators)
#                 sources_ind[item.get('source_name')] = dict(sum_ind)

#         for source, _ in sorted(sources_ind.items()):
#             new_sources_ind = list(sources_ind.keys())
#             new_sources_ind.remove(source)
#             a = set(sources_ind.get(source).keys())
#             for src in new_sources_ind:
#                 b = set(sources_ind.get(src).keys())
#                 c = a.intersection(b)
#                 intersect_weight[source].update({src: len(c) / len(a) * 100})
#         return intersect_weight


class IndicatorView(generics.ListAPIView):
    """
    (GET) Получение списка индикаторов
    """

    serializer_class = IndicatorListSerializer
    queryset = Indicator.objects.all()


class IndicatorDetailView(generics.RetrieveAPIView):
    """
    (GET) Деталка сотрудника
    """

    serializer_class = IndicatorDetailSerializer
    lookup_field = 'id'
    queryset = Indicator.objects.all()
