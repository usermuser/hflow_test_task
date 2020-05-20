import json
import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from settings import (
    RETRY_COUNT,
    RETRY_TIMEOUT,
    RETRY,
    REPEAT_TIMEOUT,
    RETRY_CODES,
    TOKEN,
    API_ENDPOINT,
)


class BaseClient:
    """Base class for clients"""

    logger = logging.getLogger(__name__)
    REQUESTS_EXCEPTIONS = (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout,
                           requests.exceptions.ConnectionError, requests.exceptions.HTTPError,
                           requests.exceptions.RequestException)

    def __init__(
            self,
            base_url=API_ENDPOINT,
            token=TOKEN,
            retry_count=RETRY_COUNT,
            retry_timeout=RETRY_TIMEOUT,
            retry=RETRY,
            repeat_timeout=REPEAT_TIMEOUT,
            retry_codes=RETRY_CODES,
    ):
        self.base_url = base_url
        self.token = token
        self.retry_count = retry_count
        self.retry_timeout = retry_timeout
        self.retry = retry
        self.repeat_timeout = repeat_timeout
        self.retry_codes = retry_codes

    def _retry_strategy(self):
        retry_methods = ("HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE")
        return Retry(
            total=self.retry_count,
            backoff_factor=self.repeat_timeout,
            status=self.retry_count,
            status_forcelist=self.retry_codes,
            connect=self.retry_count,
            read=self.retry_count,
            method_whitelist=retry_methods,
        )

    def get(self):
        pass

    def post(self, endpoint=None, json_input=True, json_output=True, payload=None):
        _url = self.base_url + endpoint

        with requests.Session() as session:
            session.mount(_url, HTTPAdapter(max_retries=self._retry_strategy()))

            try:
                if json_input:
                    response = requests.post(_url, json=payload)
                else:
                    response = requests.post(_url, data=payload)

                response.raise_for_status()



