"""Services for indicator app"""

from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response

from console_api.config.logger_config import logger
from console_api.indicator.models import Indicator, IndicatorActivities


def get_indicator_or_error_response(indicator_id: int) -> Indicator | Response:
    """Return indicator or response with 400 error if not exists"""

    return (
        Indicator.objects.get(id=indicator_id)
        if Indicator.objects.filter(id=indicator_id, deleted_at=None).exists()
        else Response(
            {"detail": f"Indicator with id {indicator_id} doesn't exists"},
            status=HTTP_400_BAD_REQUEST,
        )
    )


def create_indicator_activity(data: dict) -> None:
    """Create IndicatorActivities object"""

    activity = IndicatorActivities(
        id=IndicatorActivities.objects.order_by("id").last().id + 1,
        indicator_id=data.get("indicator_id"),
        activity_type=data.get("activity_type"),
        created_by=data.get("created_by"),
        details=data.get("details"),
    )
    activity.save()

    logger.info(f"Created indicator activity: {activity.id}")
