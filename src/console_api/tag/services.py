"""Services for tag app"""
from typing import List
from datetime import datetime

from rest_framework.request import Request

from console_api.indicator.models import Indicator
from console_api.tag.models import Tag, IndicatorTagRelationship
from console_api.indicator.services import create_indicator_activity


def get_new_tag_id() -> int:
    """Return id for new tag"""

    if Tag.objects.count() == 0:
        tag_id = 1
    else:
        tag_id = Tag.objects.order_by("id").last().id + 1

    return tag_id


def calculate_tags_weight(tag_id: int, updated_at: datetime, request: Request):
    relationship: List[IndicatorTagRelationship] = IndicatorTagRelationship.objects.filter(
        tag_id=tag_id, is_deleted=False
    )
    tags: List[Tag] = Tag.objects.filter(id__in=[tag.tag_id for tag in relationship if not tag.is_deleted])
    Indicator.objects.filter(id__in=[indicator.indicator_id for indicator in relationship]).update(
        tags_weight=max(tag.weight for tag in tags) / 100 if tags else 0,
        updated_at=updated_at
    )
    for rel in relationship:
        create_indicator_activity(
            {
                "indicator_id": rel.indicator_id,
                "activity_type": "update-indicator-tags-weight",
                "created_by": request.user.id,
                "details": request.data.get("details"),
            }
        )
