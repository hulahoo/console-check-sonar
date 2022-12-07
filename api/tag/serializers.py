from rest_framework import serializers
from src.tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = []
