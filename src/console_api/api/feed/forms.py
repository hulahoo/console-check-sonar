from django import forms

from apps.feed.models import Feed


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        exclude = ["indicators", "parsing_rules"]
