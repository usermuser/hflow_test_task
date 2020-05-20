import json
import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from settings import TOKEN

from rpsos.settings import (
    RETRY_COUNT,
    RETRY_TIMEOUT,
    RETRY,
    REPEAT_TIMEOUT,
    RETRY_CODES,
    JWT_DEFAULT_TOKEN
)


class BaseClient:
    """Base class for clients"""

    logger = logging.getLogger(__name__)
    REQUESTS_EXCEPTIONS = (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout,
                           requests.exceptions.ConnectionError, requests.exceptions.HTTPError,
                           requests.exceptions.RequestException)

    def __init__(
            self,
            base_url=None,
            token=TOKEN,
            retry_count=RETRY_COUNT,
            retry_timeout=RETRY_TIMEOUT,
            retry=RETRY,
            repeat_timeout=REPEAT_TIMEOUT,
            retry_codes=RETRY_CODES,
            ):
