"""Serializers for indicator app"""

from typing import List

from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework import serializers

from console_api.indicator.models import Indicator
from console_api.config.logger_config import logger
from console_api.tag.models import Tag, IndicatorTagRelationship
from console_api.feed.models import Feed, IndicatorFeedRelationship
from console_api.indicator.services import create_indicator_activity


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
    """Serializer for IndicatorsView view for get method"""

    def to_representation(self, instance):
        """Convert representation from null to valid value"""

        data = super().to_representation(instance)

        if not data['updated-at']:
            data['updated-at'] = data['created-at']

        if not data['ioc-weight']:
            data['ioc-weight'] = 0

        if not data['tags-weight']:
            data['tags-weight'] = 0

        return data

    class Meta:
        """Metainformation about the serializer"""

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

    def to_representation(self, instance):
        """Convert representation from null to valid value"""

        data = super().to_representation(instance)

        if not data['context']:
            data['context'] = {}

        if not data['updated-at']:
            data['updated-at'] = data['created-at']

        if not data['last-time-actuation']:
            data['last-time-actuation'] = data['updated-at']

        if not data['first-time-actuation']:
            data['first-time-actuation'] = data['created-at']

        if not data['external-source-link']:
            data['external-source-link'] = ""

        if not data['ioc-weight']:
            data['ioc-weight'] = 0

        if not data['tags-weight']:
            data['tags-weight'] = 0

        return data

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
            "is-false-positive",
            "feeds",
            "activities",
            "last-time-actuation",
            "first-time-actuation",
        ]

        extra_kwargs = {
            "ioc-type": {"source": "ioc_type"},
            "is-false-positive": {"source": "is_false_positive"},
            "is-sending-to-detections": {"source": "is_sending_to_detections"},
            "created-at": {"source": "created_at"},
            "updated-at": {"source": "updated_at"},
            "ioc-weight": {"source": "weight"},
            "tags": {"source": "tags_ids"},
            "tags-weight": {"source": "tags_weight"},
            "external-source-link": {"source": "external_source_link"},
            "last-time-actuation": {"source": "last_detected_at"},
            "first-time-actuation": {"source": "first_detected_at"},
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
        request = self.context.get("request")
        tags_id_list = validated_data.pop("tags")
        tags: List[Tag] = Tag.objects.filter(pk__in=tags_id_list)
        logger.info(f"Retrieved tags: {tags}")

        if len(tags) != len(tags_id_list):
            raise serializers.ValidationError(
                detail={"data": "No tags found with provided ids"},
                code=status.HTTP_400_BAD_REQUEST
            )

        validated_data["tags_weight"] = sum(tag.weight for tag in tags)
        validated_data["feeds_weight"] = 100

        try:
            indicator = Indicator.objects.create(**validated_data)
            create_indicator_activity({
                "indicator_id": indicator.id,
                "activity_type": "Create indicator",
                "created_by": request.user.id,
                "details": request.data.get("details"),
            })
            logger.info(f"Created indicator: {indicator.id}")
        except IntegrityError as error:
            raise serializers.ValidationError(
                detail=error, code=status.HTTP_400_BAD_REQUEST
            )

        for tag in tags:
            IndicatorTagRelationship.objects.create(
                indicator_id=indicator.id,
                tag_id=tag.id
            )
            create_indicator_activity({
                "indicator_id": indicator.id,
                "activity_type": "Added tag",
                "created_by": request.user.id,
                "details": {"tag": tag.id},
            })

        IndicatorFeedRelationship.objects.create(
            indicator_id=indicator.id,
            feed_id=-1
        )
        create_indicator_activity({
                "indicator_id": indicator.id,
                "activity_type": "Added Internal TI feed",
                "created_by": request.user.id,
                "details": {},
            })

        return indicator
