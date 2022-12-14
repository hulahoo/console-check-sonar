import os
from setuptools import setup

install_requires = [
    ('Django', '4.0.4'),
    ('django-filter', '22.1'),
    ('django-cors-headers', '3.13.0')
    ('drf-yasg', '1.21.4'),
    ('django-rest-swagger', '2.2.0')
    ('pydantic', '1.10.2'),
    ('loguru', '0.6.0'),
    ('python-dotenv', '0.21.0'),
    ('psycopg2-binary', '2.9.3'),
    ('requests', '2.27.1'),
    ('beautifulsoup4', '4.11.1'),
    ('stix2-elevator', '4.1.7'),
    ('stix2', '3.0.1'),
    ('flatdict', '4.0.1'),
]

CI_PROJECT_NAME = os.environ.get("CI_PROJECT_NAME", "сonsole-api")
ARTIFACT_VERSION = os.environ.get("ARTIFACT_VERSION", "local")
CI_PROJECT_TITLE = os.environ.get("CI_PROJECT_TITLE", "Консоль мониторинга и управления")
CI_PROJECT_URL = os.environ.get("CI_PROJECT_URL", "https://gitlab.in.axept.com/rshb/console-api")


setup(
    name=CI_PROJECT_NAME,
    version=ARTIFACT_VERSION,
    description=CI_PROJECT_TITLE,
    url=CI_PROJECT_URL,
    install_requires=[">=".join(req) for req in install_requires],
    python_requires=">=3.9.1",
    entry_points={
        'console_scripts': [
            CI_PROJECT_NAME + " = " + "console_api.main:execute"
        ]
    }
)
