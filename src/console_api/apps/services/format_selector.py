from console_api.apps.services.parsers.csv import parse_csv
from console_api.apps.services.parsers.text import parse_free_text
from console_api.apps.services.parsers.json import parse_custom_json
from console_api.apps.services.parsers.stix import parse_stix
from console_api.apps.services.parsers.misp import parse_misp

methods = {
    "json": parse_custom_json,
    "stix": parse_stix,
    "free_text": parse_free_text,
    "misp": parse_misp,
    "csv": parse_csv,
    "txt": parse_free_text
}


def choose_type(name: str):
    return methods[name]
