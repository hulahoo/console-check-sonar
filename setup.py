import os
from setuptools import setup

setup(
    name=os.environ["CI_PROJECT_NAME"],
    version="local",
    description=os.environ["CI_PROJECT_TITLE"],
    url=os.environ["CI_PROJECT_URL"],
    install_requires=[
        "Django==4.0.4",
        "psycopg2-binary>=2.9.3",
        "requests>=2.27.1",
        "beautifulsoup4>=4.11.1",
        "stix2-elevator>=4.1.7",
        "stix2>=3.0.1",
        "flatdict>=4.0.1",
        "django-filter>=22.1",
        "drf-yasg>=1.21.4",
        "flatdict>=4.0.1",
        "django-rest-swagger>=2.2.0"
    ],
    entry_points={
        'console_scripts': [
            os.environ["CI_PROJECT_NAME"] +
            " = " +
            os.environ["CI_PROJECT_NAME"] +
            ":main"
        ]
    }
)
