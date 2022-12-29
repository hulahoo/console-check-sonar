"""Services for statistics app"""

from datetime import datetime

from rest_framework.request import Request

from console_api.api.statistics.constants import MINUTE_PERIOD_FORMAT


def get_period_query_params(request: Request) -> tuple:
    """Return start_period_at and finish_period_at query params"""

    start_period_at = datetime.strptime(
        request.GET.get('start-period-at'),
        MINUTE_PERIOD_FORMAT,
    )

    finish_period_at = datetime.strptime(
        request.GET.get('finish-period-at'),
        MINUTE_PERIOD_FORMAT,
    )

    return start_period_at, finish_period_at
