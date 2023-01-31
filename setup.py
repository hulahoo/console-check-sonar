import os
from setuptools import setup

install_requires = [
    ('Django', '4.0.4'),
    ('environs', '9.5.0'),
    ('psycopg2-binary', '2.9.3'),
    ('requests', '2.27.1'),
    ('djangorestframework', '3.13.1'),
    ('beautifulsoup4', '4.11.1'),
    ('stix2-elevator', '4.1.7'),
    ('stix2', '3.0.1'),
    ('prometheus-client', '0.15.0'),
    ('django-filter', '22.1'),
    ('drf-yasg', '1.21.4'),
    ('flatdict', '4.0.1'),
    ('django-debug-toolbar', '3.7.0'),
    ('django-rest-swagger', '2.2.0'),
    ('django-cors-headers', '3.13.0'),
    ('gunicorn', '20.1.0'),
    ('pandas', '1.4.3')
]

CI_PROJECT_NAME = os.environ.get("CI_PROJECT_NAME", "console-api")
ARTIFACT_VERSION = os.environ.get("ARTIFACT_VERSION", "local")
CI_PROJECT_TITLE = os.environ.get("CI_PROJECT_TITLE", "Консоль мониторинга и управления")
CI_PROJECT_URL = os.environ.get("CI_PROJECT_URL", "https://gitlab.in.axept.com/rshb/console-api")


setup(
    name=CI_PROJECT_NAME,
    version=ARTIFACT_VERSION,
    description=CI_PROJECT_TITLE,
    url=CI_PROJECT_URL,
    install_requires=[">=".join(req) for req in install_requires],
    python_requires=">=3.11.1",
    entry_points={
        'console_scripts': [
            CI_PROJECT_NAME + " = " + "console_api.main:execute"
        ]
    }
)
