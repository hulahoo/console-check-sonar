import json
from uuid import uuid4

from stix2elevator import elevate

from console_api.config.logger_config import logger
from console_api.indicator.models import Indicator
from console_api.feed.services.ext import get_url, feed_control


def get_or_elevate(feed) -> dict:
    """
    Узнает версию stix и переводит во вторую версию.
    """
    text = get_url(feed.link)
    try:
        return json.loads(text)
    except Exception as e:
        logger.info(f"Error is: {e}")
        return elevate(text)


def parse_stix(feed, config: dict = None):
    """
    Парсит переданный json в формате STIX и отдает список индикаторов.
    """

    if not config:
        config = {}

    limit = config.get('limit')

    bundle = get_or_elevate(feed)
    objects = bundle.get("objects")
    if limit:
        objects = list(objects)[:limit]

    raw_indicators = [obj for obj in objects if obj.get("type") == "indicator"]
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
