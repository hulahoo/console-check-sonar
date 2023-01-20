"""Serializers for indicator app"""

from rest_framework import serializers

from console_api.feed.models import Feed, IndicatorFeedRelationship
from console_api.tag.models import Tag
from console_api.indicator.models import Indicator


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["title", "weight"]
        exclude = []


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ["title"]
        exclude = []


class IndicatorFeedSerializer(serializers.ModelSerializer):
    """Serializer for model IndicatorFeedRelationship"""

    class Meta:
        """Metainformation for serializer"""

        model = IndicatorFeedRelationship

        fields = ["type", "details", "created_at"]

        extra_kwargs = {
            "created-at": {"source": "created_at"},
        }


class IndicatorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator

        fields = [
            "id",
            "ioc-type",
            "value",
            "created-at",
            "updated-at",
            "ioc-weight",
            "tags",
            "tags-weight",
            "feed-names",
        ]

        extra_kwargs = {
            "ioc-type": {"source": "ioc_type"},
            "created-at": {"source": "created_at"},
            "updated-at": {"source": "updated_at"},
            "ioc-weight": {"source": "weight"},
            "tags": {"source": "tags_ids"},
            "tags-weight": {"source": "tags_weight"},
            "feed-names": {"source": "feeds_names"},
        }


class IndicatorDetailSerializer(serializers.ModelSerializer):
    """Serializer for IndicatorDetailView"""

    class Meta:
        """Metainformation about the serializer"""

        model = Indicator

        fields = [
            "id",
            "ioc-type",
            "value",
            "context",
            "created-at",
            "updated-at",
            "ioc-weight",
            "tags",
            "tags-weight",
            "external-source-link",
            "feeds",
            "activities",
        ]

        extra_kwargs = {
            "ioc-type": {"source": "ioc_type"},
            "created-at": {"source": "created_at"},
            "updated-at": {"source": "updated_at"},
            "ioc-weight": {"source": "weight"},
            "tags": {"source": "tags_ids"},
            "tags-weight": {"source": "tags_weight"},
            "external-source-link": {"source": "external_source_link"},
        }


class IndicatorCreateSerializer(serializers.ModelSerializer):
    """Serializer for indicator creation"""

    class Meta:
        """Metainformation about the serializer"""

        model = Indicator

        fields = [
            "ioc-type",
            "value",
            "context",
            "tags",
        ]

        extra_kwargs = {
            "ioc-type": {"source": "ioc_type"},
        }


class IndicatorDetailSerializer(serializers.ModelSerializer):
    """Serializer for detail indiactor"""

    class Meta:
        """Metainformation about the serializer"""

        model = Indicator

        fields = [
            "id",
            "ioc-type",
            "value",
            "context",
            "created-at",
            "updated-at",
            "ioc-weight",
            "tags",
            "tags-weight",
            "external-source-link",
            "feeds",
            "activities",
        ]

        extra_kwargs = {
            "ioc-type": {"source": "ioc_type"},
            "created-at": {"source": "created_at"},
            "updated-at": {"source": "updated_at"},
            "tags": {"source": "tags_ids"},
            "ioc-weight": {"source": "weight"},
            "tags-weight": {"source": "tags_weight"},
            "external-source-link": {"source": "external_source_link"},
        }
