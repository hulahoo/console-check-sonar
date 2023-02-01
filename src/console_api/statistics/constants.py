"""Constants for statistics app"""

MINUTE_PERIOD_FORMAT = "%Y-%m-%d %H:%M"

HOUR_PERIOD_FORMAT = "%Y-%m-%d %H"

DAY_PERIOD_FORMAT = "%Y-%m-%d"

MONTH_PERIOD_FORMAT = "%Y-%m"

GROUP_BY_AND_FREQUENCY = {
    "minute": "T",
    "hour": "H",
    "day": "D",
    "month": "MS",
}

FREQUENCY_AND_FORMAT = {
    "T": MINUTE_PERIOD_FORMAT,
    "H": HOUR_PERIOD_FORMAT,
    "12H": HOUR_PERIOD_FORMAT,
    "D": DAY_PERIOD_FORMAT,
    "MS": MONTH_PERIOD_FORMAT,
}
