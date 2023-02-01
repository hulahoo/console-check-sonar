"""Constants for the project"""

from keyword import kwlist


CREDS_ERROR = "Authentication credentials were not provided."
SEARCH_QUERY_ERROR = "Missing or empty 'query' param"

ADMIN_PASS_HASH = \
    "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

ADMIN_LOGIN = "admin"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

class TestClass:
    """Empty class for testing"""


def test_function():
    """Empty function for testing"""

KEYWORDS = (
    'class', 'list', 'tuple', 'set', 'dict', 'arrow', 'str', 'int',
    'type', 'float',
) + tuple([str(keyword) for keyword in kwlist])

NOT_STRING_VALUES = (
    # int, float and bool
    0, 100_000, -100, 122.12323, True, False,

    # Data structures
    [1, 2, 3], (1, 2), {'a': 1, 'b': 2}, set([1, 2, 3]), [[1, 2, 3, (1, 2)]],

    # Types
    int, bool, str, object, bytes, bytearray, tuple, list, dict, set, float,

    # Classes and functions
    TestClass, test_function, lambda x: x,

    # Others
    None, complex(1, 2), bin(20), hex(100), range(100),
)

WRONG_PAGE_SIZE = (
    # int, float and bool
    -100, 122.12323, True, False,

    # Data structures
    [1, 2, 3], (1, 2), {'a': 1, 'b': 2}, set([1, 2, 3]), [[1, 2, 3, (1, 2)]],

    # Types
    int, bool, str, object, bytes, bytearray, tuple, list, dict, set, float,

    # Classes and functions
    TestClass, test_function, lambda x: x,

    # Others
    None, complex(1, 2), bin(20), hex(100), range(100),

    'value   value', '!@@#Q@$Q', 'test'.encode(), 'a', 'b', 'A', 'B', 'def',
)

DIFFERENT_STRINGS = (
    'value   value', '!@@#Q@$Q', 'test'.encode(), 'a', 'b', 'A', 'B', 'def'
)

DIFFERENT_VALUES = DIFFERENT_STRINGS + NOT_STRING_VALUES
