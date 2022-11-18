from django_filters import rest_framework as filters

from src.feed.models import Feed


class FeedFilter(filters.FilterSet):
    class Meta:
        model = Feed
        fields = Feed.get_model_fields()
        exclude = ['sertificate']
