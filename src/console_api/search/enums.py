from enum import Enum


class SearchStatus(str, Enum):
    DETECTED = 'detected'
    NOT_DETECTED = 'not-detected'
