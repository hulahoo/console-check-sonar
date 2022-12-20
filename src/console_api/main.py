import os
import subprocess

import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "console_api.settings.settings")

django.setup()


def execute():
    """
    Function apply migrations:
    """
    # call_command('migrate')
    call_command(subprocess.call(['gunicorn', '-b 0.0.0.0:8080', 'console_api.settings.wsgi:application', '--workers=4']))
