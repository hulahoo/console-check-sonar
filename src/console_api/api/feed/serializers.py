from rest_framework import serializers

from console_api.apps.feed.models import Feed


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed

        fields = [
            "id",
            "source-url",
            "format",
            "use-taxii",
            "polling-frequency",
            "auth-type",
            "auth-api-token",
            "auth-login",
            "auth-pass",
            "certificate",
            "parsing-rules",
            "feed-name",
            "provider",
            "description",
            "is-enabled",
            "status",
            "is-truncating",
            "max-records-count",
            "weight",
            "available-fields",
            # "importing-fields",
            "created-at",
        ]

        extra_kwargs = {
            'source-url': {'source': 'url'},
            'use-taxii': {'source': 'use_taxii'},
            "polling-frequency": {'source': "polling_frequency"},
            "auth-type": {'source': "auth_type"},
            "auth-api-token": {'source': "auth_api_token"},
            "auth-login": {'source': "auth_login"},
            "auth-pass": {'source': "auth_pass"},
            "parsing-rules": {'source': "parsing_rules"},
            "feed-name": {'source': "title"},
            "is-enabled": {'source': "is_active"},
            "is-truncating": {'source': "is_truncating"},
            "max-records-count": {'source': "max_records_count"},
            "available-fields": {'source': "available_fields"},
            "created-at": {'source': "created_at"},
        }


class DashboardFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ['title', 'ts']
        exclude = []


class FeedShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ['id', 'name']

        extra_kwargs = {
            'name': {'source': 'title'},
        }
