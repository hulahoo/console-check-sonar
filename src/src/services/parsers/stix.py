import json
from uuid import uuid4

from stix2elevator import elevate

from src.indicator.models import Indicator
from src.services.ext import get_url, feed_control


def get_or_elevate(feed) -> dict:
    """
    Узнает версию stix и переводит во вторую версию.
    """
    text = get_url(feed.link)
    try:
        return json.loads(text)
    except Exception as e:
        return elevate(text, f"Error is: {e}")


def parse_stix(feed, raw_indicators=None, config: dict = {}):
    """
    Парсит переданный json в формате STIX и отдает список индикаторов.
    """

    limit = config.get('limit', None)

    bundle = get_or_elevate(feed)
    objects = bundle.get("objects")
    raw_indicators = []

    if limit:
        objects = list(objects)[:limit]

    for obj in objects:
        if obj.get("type") == "indicator":
            raw_indicators.append(obj)

    indicators = []
    feed_control(feed, config)
    for raw_indicator in raw_indicators:
        indicator, created = Indicator.objects.get_or_create(value=raw_indicator.get("name"),
                                                             defaults={
                                                                 "uuid": raw_indicator.get('id', uuid4()),
                                                                 "first_detected_date": raw_indicator.get("created"),
                                                                 "supplier_name": feed.vendor,
                                                                 "supplier_confidence": feed.confidence,
                                                                 "weight": feed.confidence
                                                             }
                                                             )

        indicator.feeds.add(feed)
        pattern = raw_indicator.get("pattern")
        if "ip" in pattern:
            indicator.ioc_context_ip = pattern
            indicator.type = "IP"
        elif "filesize" in pattern:
            indicator.ioc_context_file_size = pattern
        indicator.save()
        indicators.append(indicator)
    return indicators
