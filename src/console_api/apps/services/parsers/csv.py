import csv
from uuid import uuid4

from stix2elevator.options import initialize_options

from apps.indicator.models import Indicator
from apps.services.ext import feed_control

initialize_options(options={"spec_version": "2.1"})


def parse_csv(feed, raw_indicators=None, config: dict = {}) -> list:
    """
    Парсит переданный текст с параметрами для csv и отдает список индикаторов.
    """
    limit = config.get('limit', 0)

    raw_indicators = [
        row for row in raw_indicators.split("\n") if not row.startswith("#")
    ]
    indicators = []
    feed_control(feed, config)

    counter = 0

    for row in csv.DictReader(
            raw_indicators,
            delimiter=config.get('delimiter', ","),
            fieldnames=config.get('fieldnames', ""),
            dialect=config.get('dialect', "excel"),
    ):
        indicator, created = Indicator.objects.get_or_create(value=row.get(feed.custom_field), defaults={
            "uuid": uuid4,
            "supplier_name": feed.vendor,
            "supplier_confidence": feed.confidence,
            "weight": feed.confidence
        })
        indicator.feeds.add(feed)

        counter += 1
        if counter >= limit > 0:
            break

    return indicators
