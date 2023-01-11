"""WSGI config for the project"""

from os import environ

from django.core.wsgi import get_wsgi_application


environ.setdefault('DJANGO_SETTINGS_MODULE', 'console_api.config.settings')

application = get_wsgi_application()
