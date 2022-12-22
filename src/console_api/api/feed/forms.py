from django import forms

from console_api.apps.feed.models import Feed


class FeedForm(forms.ModelForm):
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
            "importing-fields",
        ]
