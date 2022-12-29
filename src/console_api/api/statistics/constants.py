"""Constants for statistics app"""

MINUTE_PERIOD_FORMAT = "%Y-%m-%d %H:%M"

HOUR_PERIOD_FORMAT = "%Y-%m-%d %H"

DAY_PERIOD_FORMAT = "%Y-%m-%d"

FREQUENCY_AND_FORMAT = {
    "T": MINUTE_PERIOD_FORMAT,
    "H": HOUR_PERIOD_FORMAT,
    "12H": HOUR_PERIOD_FORMAT,
    "D": DAY_PERIOD_FORMAT,
}
