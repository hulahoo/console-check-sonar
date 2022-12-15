import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

import django
django.setup()

from django.core.management import call_command


def execute():
    """
    Function apply migrations:
    """
    call_command('migrate')
