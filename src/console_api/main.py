import os
import subprocess

import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

django.setup()


def execute():
    """
    Function apply migrations:
    """
    call_command('collectstatic')
    call_command('migrate')
    call_command(subprocess.call(['gunicorn', 'wsgi:application', '--bind 0.0.0.0:8080', '--workers=4']))
