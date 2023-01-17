"""Serializers for feed app"""

from rest_framework import serializers

from console_api.feed.models import Feed


class FeedCreateSerializer(serializers.ModelSerializer):
    """Serializer for feed creation"""

    class Meta:
        """Metainformation about the serializer"""

        model = Feed

        fields = [
            "source-url",
            "format",
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
            "is-truncating",
            "max-records-count",
            "weight",
            "available-fields",
            "is-use-taxii",
        ]

        extra_kwargs = {
            'source-url': {'source': 'url'},
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
            "is-use-taxii": {'source': "is_use_taxii"}
        }


class FeedsListSerializer(serializers.ModelSerializer):
    """Serializer for list of feeds"""

    class Meta:
        """Metainformation about the serializer"""

        model = Feed

        fields = [
            "id",
            "source-url",
            "format",
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
            "is-truncating",
            "max-records-count",
            "weight",
            "available-fields",
            "is-use-taxii",
            "polling-frequency",
            "status",
            "importing-fields",
            "created-at"
        ]

        extra_kwargs = {
            'source-url': {'source': 'url'},
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
            "is-use-taxii": {'source': "is_use_taxii"},
            "importing-fields": {'source': "importing_fields"},
            "created-at": {'source': "created_at"},
        }


class FeedUpdatePropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed

        fields = [
            "source-url",
            "format",
            "use-taxii",
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
            "is-truncating",
            "max-records-count",
            "weight",
            "importing-fields"
        ]

        extra_kwargs = {
            "source-url": {"source": "url"},
            "use-taxii": {'source': "is_use_taxii"},
            "auth-type": {'source': "auth_type"},
            "auth-api-token": {'source': "auth_api_token"},
            "auth-login": {'source': "auth_login"},
            "auth-pass": {'source': "auth_pass"},
            "parsing-rules": {'source': "parsing_rules"},
            "feed-name": {'source': "title"},
            "is-enabled": {'source': "is_active"},
            "is-truncating": {'source': "is_truncating"},
            "max-records-count": {'source': "max_records_count"},
            "importing-fields": {'source': "importing_fields"}
        }
