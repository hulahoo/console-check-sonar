from rest_framework import serializers

from apps.indicator.models import Indicator
from apps.tag.models import Tag
from apps.feed.models import Feed


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['title', 'weight']
        exclude = []


class FeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feed
        fields = ['name']
        exclude = []


class IndicatorSerializer(serializers.ModelSerializer):
    tags = TagSerializer()
    feeds = FeedSerializer()

    class Meta:
        model = Indicator
        fields = ['uuid', 'type_indicator', 'value',
                  'created_at', 'updated_at',
                  'weight', 'tags', 'feeds']
        exclude = []
