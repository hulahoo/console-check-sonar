from rest_framework import serializers

from apps.feed.models import Feed


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        exclude = []


class DashboardFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ['name', 'ts']
        exclude = []
