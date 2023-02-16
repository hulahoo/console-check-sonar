"""Services for files app"""

import calendar
import time
import hashlib


def get_time_prefix() -> int:
    return calendar.timegm(time.gmtime())


def update_key_with_ts(file_name: str) -> str:
    file_name = file_name.split('.')
    file_name = file_name[0] + '_' + str(get_time_prefix()) + '.' + file_name[1]
    return file_name


def get_hash(file_content):

    file_hash_md5 = hashlib.md5()
    file_hash_md5.update(file_content)

    file_hash_sha1 = hashlib.sha1()
    file_hash_sha1.update(file_content)

    file_hash_sha256 = hashlib.sha256()
    file_hash_sha256.update(file_content)

    return file_hash_md5.hexdigest(),file_hash_sha1.hexdigest(),file_hash_sha256.hexdigest()
