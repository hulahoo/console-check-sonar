from rest_framework import serializers

from src.feed.models import Feed


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        exclude = []
