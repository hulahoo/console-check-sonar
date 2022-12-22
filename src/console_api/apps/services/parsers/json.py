import json
from uuid import uuid4

from flatdict import FlatterDict

from console_api.apps.services.ext import feed_control, get_url
from console_api.apps.indicator.models import Indicator


def parse_custom_json(feed, config: dict = {}):
    """
    Парсит переданный кастомный json с выбранными из фида полями и отдает список индикаторов.
    """
    limit = config.get('limit', None)

    feed_control(feed, config)
    raw_json = json.loads(get_url(feed.link))
    indicators = []

    if limit:
        lst = list(FlatterDict(raw_json).items())[:limit]
    else:
        lst = list(FlatterDict(raw_json).items())

    for key, value in lst:
        indicator, created = Indicator.objects.get_or_create(value=value, defaults={
            "uuid": uuid4(),
            "supplier_name": feed.vendor,
            "supplier_confidence": feed.confidence,
            "weight": feed.confidence
        })
        indicator.feeds.add(feed)
        indicators.append(indicator)
    return indicators
