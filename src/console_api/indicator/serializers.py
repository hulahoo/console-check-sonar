"""Serializers for indicator app"""

from typing import List

from rest_framework import status
from rest_framework import serializers

from console_api.indicator.models import Indicator
from console_api.config.logger_config import logger
from console_api.tag.models import Tag, IndicatorTagRelationship
from console_api.feed.models import Feed, IndicatorFeedRelationship


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
            "is-false-positive",
            "is-archived",
        ]

        extra_kwargs = {
            "ioc-type": {"source": "ioc_type"},
            "created-at": {"source": "created_at"},
            "updated-at": {"source": "updated_at"},
            "ioc-weight": {"source": "weight"},
            "tags": {"source": "tags_ids"},
            "is-false-positive": {"source": "is_false_positive"},
            "is-archived": {"source": "is_archived"},
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
            "is-sending-to-detections",
            "tags",
            "tags-weight",
            "external-source-link",
            "feeds",
            "activities",
        ]

        extra_kwargs = {
            "ioc-type": {"source": "ioc_type"},
            "is-sending-to-detections": {"source": "is_sending_to_detections"},
            "created-at": {"source": "created_at"},
            "updated-at": {"source": "updated_at"},
            "ioc-weight": {"source": "weight"},
            "tags": {"source": "tags_ids"},
            "tags-weight": {"source": "tags_weight"},
            "external-source-link": {"source": "external_source_link"},
        }


class IndicatorCreateSerializer(serializers.Serializer):
    """Serializer for indicator creation"""
    tags = serializers.ListField(
        child=serializers.IntegerField(min_value=0, required=True)
    )
    ioc_type = serializers.CharField(max_length=32, required=True)
    value = serializers.CharField(max_length=1024, required=True)
    context = serializers.JSONField(required=True)

    def create(self, validated_data):
        tags_id_list = validated_data.pop("tags")
        tags: List[Tag] = Tag.objects.filter(pk__in=tags_id_list)
        logger.info(f"Retrieved tags: {tags}")
        if len(tags) != len(tags_id_list):
            raise serializers.ValidationError(
                detail={"data": "No tags found with provided ids"},
                code=status.HTTP_400_BAD_REQUEST
            )
        validated_data["tags_weight"] = sum([tag.weight for tag in tags])
        indicator = Indicator.objects.create(**validated_data)
        logger.info(f"Created indicator: {indicator.id}")
        for tag in tags:
            IndicatorTagRelationship.objects.create(
                indicator_id=indicator.id,
                tag_id=tag.id
            )
        return indicator
