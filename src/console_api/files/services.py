"""Services for files app"""

import calendar
import time
import hashlib


def get_time_prefix() -> int:
    return calendar.timegm(time.gmtime())


def update_key_with_ts(file_name: str) -> str:
    file_name = file_name.split('.')
    updated_file_name = file_name[0] + '_' + str(get_time_prefix())
    if len(file_name) == 2:
        updated_file_name = updated_file_name + '.' + file_name[1]
    return updated_file_name


def get_hash(file_content):

    file_hash_sha256 = hashlib.sha256()
    file_hash_sha256.update(file_content)

    return file_hash_sha256.hexdigest()
