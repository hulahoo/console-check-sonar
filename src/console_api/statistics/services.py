"""Services for statistics app"""

from datetime import datetime, timedelta

from rest_framework.request import Request
from pandas import date_range

from console_api.statistics.constants import (
    FREQUENCY_AND_FORMAT,
    GROUP_BY_AND_FREQUENCY,
)


def get_datetime_from_iso(iso_date: str) -> datetime:
    """Return datetime from data in iso format"""

    dt, _, us = iso_date.partition(".")
    dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    us = int(us.rstrip("Z"), 10)

    return dt + timedelta(microseconds=us)


def get_period_query_params(request: Request) -> tuple:
    """Return start_period_at and finish_period_at query params"""

    start_period_at = request.GET.get("start-period-at")
    finish_period_at = request.GET.get("finish-period-at")

    if not start_period_at or not finish_period_at:
        return None, None

    start_period_at = get_datetime_from_iso(start_period_at)
    finish_period_at = get_datetime_from_iso(finish_period_at)

    return start_period_at, finish_period_at


def get_objects_data_for_statistics(request: Request, model) -> dict:
    """Return date and objects amount for the date"""

    group_by = request.GET.get("group-by", "minute")

    # 1 minute by default
    frequency = GROUP_BY_AND_FREQUENCY.get(group_by, "T")
    start_period_at, finish_period_at = get_period_query_params(request)

    if not start_period_at or not finish_period_at:
        return {"error": "Start or finish period not specified"}

    period_format = FREQUENCY_AND_FORMAT.get(frequency)

    if not period_format:
        return {"error": "Invalid group-by"}

    for obj in model.objects.all():
        print(obj.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    objects = model.objects.filter(
        created_at__range=(start_period_at, finish_period_at),
    )

    date_and_objects_amount = {
        date.to_pydatetime().strftime("%Y-%m-%dT%H:%M:%S.%fZ"): 0
        for date in date_range(
            start_period_at.strftime(period_format),
            finish_period_at.strftime(period_format),
            freq=frequency,
        )
    }

    for obj in objects:
        date = obj.created_at.strftime(period_format)
        date = datetime.strptime(date, period_format)
        date = date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        date_and_objects_amount[date] += 1

    return {
        "labels": list(date_and_objects_amount.keys()),
        "values": list(date_and_objects_amount.values()),
    }
