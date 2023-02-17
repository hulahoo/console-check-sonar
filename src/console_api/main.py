"""Run the project"""

from os import environ
from subprocess import call

from django import setup
from django.core.management import call_command

from console_api.config.logger_config import logger


environ.setdefault("DJANGO_SETTINGS_MODULE", "console_api.config.settings")

setup()


def execute() -> None:
    """Run the project"""

    logger.info("Start the project")

    call_command(
        call([
            "gunicorn",
            "-b 0.0.0.0:8080",
            "console_api.config.wsgi:application",
            "--workers=6",
        ])
    )
