"""Serializers for indicator app"""

from rest_framework import serializers

from console_api.platform_settings.models import PlatformSettings


class PlatformSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformSettings
        fields = [
            'id',
            'key',
            'value',
            'created_at',
            'updated_at',
            'created_by'
        ]
