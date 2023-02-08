import time
from console_api.config.logger_config import logger


def time_profiling(get_response):

    def middleware(request):
        start_time = time.monotonic()

        response = get_response(request)

        total = time.monotonic() - start_time
        logger.debug(f"Request path:{request.path}, time = {total}")

        return response

    return middleware
