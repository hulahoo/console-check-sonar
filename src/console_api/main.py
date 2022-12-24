import os
import subprocess

import django
from django.core.management import call_command

from console_api.config.log_conf import logger

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "console_api.settings.settings")

django.setup()


def execute():
    """
    Function to start Django app
    """
    logger.info("Start Django app")
    call_command(subprocess.call([
        'gunicorn', '-b 0.0.0.0:8080', 'console_api.settings.wsgi:application', '--workers=4'
    ]))
