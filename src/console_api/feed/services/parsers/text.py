from uuid import uuid4

from console_api.config.logger_config import logger
from console_api.indicator.models import Indicator


def convert_txt_to_indicator(feed, raw_indicators=None):
    if feed.format_of_feed == "TXT":
        complete_indicators = []
        feed.save()
        for raw_indicator in raw_indicators:
            indicator, created = Indicator.objects.get_or_create(value=raw_indicator,
                                                                 defaults={
                                                                     "uuid": uuid4(),
                                                                     "supplier_name": feed.vendor,
                                                                     "type": feed.type_of_feed,
                                                                     "weight": feed.confidence,
                                                                     "supplier_confidence": feed.confidence
                                                                 })
            indicator.feeds.add(feed)
            complete_indicators.append(indicator)
        return complete_indicators


def parse_free_text(feed, raw_indicators=None, config: dict = {}):
    """
    Парсит переданный текст и отдает список индикаторов.
    """
    limit = config.get('limit', None)

    raw_indicators = raw_indicators.split("\n")
    try:
        raw_indicators.remove("")
    except Exception as e:
        logger.info(f"Error is: {e}")
    raw_indicators = [
        ioc.replace("\r", "") for ioc in raw_indicators if not ioc.startswith("#")
    ]

    if limit:
        raw_indicators = raw_indicators[:limit]

    result = convert_txt_to_indicator(feed, raw_indicators)
    return result
