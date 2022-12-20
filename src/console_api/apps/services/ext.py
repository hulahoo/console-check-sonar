import requests

from config.log_conf import logger
from apps.feed.models import Feed


def get_url(url) -> str:
    """
    Опрашивает переданный url и возвращает всю страницу в строковом формате.
    """
    try:
        received_data = requests.get(url).text
    except Exception as e:
        logger.error(f"Error is: {e}")
    return received_data


def feed_control(feed, config):
    fields = ['type_of_feed', 'format_of_feed', 'auth_type', 'polling_frequency', 'auth_login', 'auth_password',
              'ayth_querystring', 'separator', 'custom_field', 'sertificate', 'vendor', 'name', 'link', 'confidence',
              'records_quantity', 'update_status', 'ts', 'source_id']

    if config.get('is_instead_full', False):
        Feed.objects.filter(name=feed.name).delete()
        feed.save()
    else:
        feed_exist = Feed.objects.filter(name=feed.name).first()
        if feed_exist:
            for field in fields:
                setattr(feed_exist, field, getattr(feed, field))
            feed = feed_exist
        else:
            feed.save()
    return feed
