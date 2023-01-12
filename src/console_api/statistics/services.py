"""Services for statistics app"""

from datetime import datetime

from rest_framework.request import Request
from pandas import date_range

from console_api.statistics.constants import (
    FREQUENCY_AND_FORMAT,
    MINUTE_PERIOD_FORMAT,
)


def get_period_query_params(request: Request) -> tuple:
    """Return start_period_at and finish_period_at query params"""

    start_period_at = request.GET.get("start-period-at")
    finish_period_at = request.GET.get("finish-period-at")

    if not start_period_at or not finish_period_at:
        return None, None

    start_period_at = datetime.strptime(start_period_at, MINUTE_PERIOD_FORMAT)
    finish_period_at = datetime.strptime(finish_period_at, MINUTE_PERIOD_FORMAT)

    return start_period_at, finish_period_at


def get_objects_data_for_statistics(request: Request, model) -> dict:
    """Return date and objects amount for the date"""

    # 1 minute by default
    frequency = request.GET.get("frequency", "T")
    start_period_at, finish_period_at = get_period_query_params(request)

    if not start_period_at or not finish_period_at:
        return {"error": "Start or finish period not specified"}

    period_format = FREQUENCY_AND_FORMAT.get(frequency)

    if not period_format:
        return {"error": "Invalid frequency"}

    objects = model.objects.filter(
        created_at__range=(start_period_at, finish_period_at),
    )

    date_and_objects_amount = {
        str(date.strftime(period_format)): 0
        for date in date_range(
            start_period_at.strftime(period_format),
            finish_period_at.strftime(period_format),
            freq=frequency,
        )
    }

    for obj in objects:
        date = obj.created_at.strftime(period_format)
        date_and_objects_amount[date] += 1

    return {
        "labels": list(date_and_objects_amount.keys()),
        "values": list(date_and_objects_amount.values()),
    }
