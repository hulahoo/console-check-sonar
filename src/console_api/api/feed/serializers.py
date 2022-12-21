from rest_framework import serializers

from apps.feed.models import Feed


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed

        fields = [
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
            # TODO: хз с каким полем модели ассоциируется, узнать
            # "importing-fields",
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
            "is-truncating": {'source': "is-truncating"},
            "max-records-count": {'source': "max_records_count"},
        }


class DashboardFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ['name', 'ts']
        exclude = []


class FeedShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ['id', 'title']
