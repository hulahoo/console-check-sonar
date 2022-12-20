import json

from bs4 import BeautifulSoup

from apps.services.ext import get_url
from config.log_conf import logger
from apps.indicator.models import Indicator


def parse_misp_event(urls_for_parsing, feed):
    """
    Парсит MISP евенты со страницы с url'ами.
    """
    indicators = []
    for url in urls_for_parsing:
        indicators.append(convert_misp_to_indicator(json.loads(get_url(url)), feed))
    return indicators


def convert_misp_to_indicator(feed, raw_indicators=None):
    """
    Из MISP события и входящих в него параметров и объектов -
    импортирует список индиктаторов
    """
    indicators = []
    attributes = raw_indicators.get("Event").get("Attribute")
    attribute_in_object = []
    if raw_indicators.get("Event").get("Object"):
        for object in raw_indicators.get("Event").get("Object"):
            attribute_in_object = object.get("Attribute")

    attributes_list = [*attributes, *attribute_in_object]
    try:
        for attribute in attributes_list:
            indicator, created = Indicator.objects.get_or_create(value=attribute.get('value'), defaults={
                "uuid": attribute.get("uuid"),
                "ioc_context_type": attribute.get("type"),
                "supplier_name": feed.vendor,
                "supplier_confidence": feed.confidence,
                "weight": feed.confidence
            })

            try:
                indicator.feeds.add(feed)
                indicators.append(indicator)
            except Exception as e:
                raise logger.info(f"Error is: {e}")
    except TypeError:

        return indicators


def parse_misp(feed, config: dict = {}) -> list:
    """
    Парсит переданный текст со списком url'ок и отдает список индикаторов.
    Применяется когда по ссылке находится список json файлов.
    """
    limit = config.get('limit', None)

    parsed_page = BeautifulSoup(get_url(feed.link), "html.parser")
    urls_for_parsing = []

    links = list(parsed_page.find_all("a"))
    if limit:
        links = links[:limit]

    for link in links:
        if ".json" in link.text:
            urls_for_parsing.append(f"{feed.link}{link.get('href')}")
    misp_events = parse_misp_event(urls_for_parsing, feed)
    return misp_events
