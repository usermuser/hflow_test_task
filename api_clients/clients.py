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
    LOGIN,
    PASSWORD,
    ACCOUNT_ID
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

    def get(self, url='', payload=None, session=None, json_output=True, **kwargs):
        """GET request with retry strategy"""
        url = self.base_url + url

        session = session or requests.Session()
        adapter = HTTPAdapter(max_retries=self._retry_strategy)
        session.mount(url, adapter=adapter)

        try:
            self.logger.debug('Делаем GET запрос по адресу %s' % url)
            response = requests.get(url, params=payload)

            if not response:
                self.logger.error('Запрос по адресу %s не удался, пустой ответ' % url)
                return None

            if response.status_code == 200:
                if json_output:
                    return response.json()

                return response

        except self.REQUESTS_EXCEPTIONS:
            self.logger.exception('Запрос по адресу %s не удался.' % url)

        except json.decoder.JSONDecodeError:
            self.logger.exception('В ответe не JSON: %s' % response)

        except Exception:
            self.logger.exception('Внутренняя ошибка!')

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
                return response.json()
            except self.REQUESTS_EXCEPTIONS:
                self.logger.exception('Запрос по адресу %s не удался' % _url)
                return
            except Exception:
                self.logger.exception('Неизвестная ошибка...')
                return


class HuntFlowClient(BaseClient):

    def get_vacancies(self):
        """GET /account/{account_id}/vacancies
        вернёт список вакансий компании

        mine -
        opened -
        count, page -
        """
        account_id = LOGIN
        url = f'/account/{account_id}/'
        pass

    def add_candidate_to_db(self):
        """POST /account/{account_id}/applicants

        В теле запроса необходимо передать JSON вида:
            {
                "last_name": "Глибин",
                "first_name": "Виталий",
                "middle_name": "Николаевич",
                "phone": "89260731778",
                "email": "glibin.v@gmail.com",
                "position": "Фронтендер",
                "company": "ХХ",
                "money": "100000 руб",
                "birthday_day": 20,
                "birthday_month": 7,
                "birthday_year": 1984,
                "photo": 12341,
                "externals": [
                    {
                        "data": {
                            "body": "Текст резюме\nТакой текст"
                        },
                        "auth_type": "NATIVE",
                        "files": [
                            {
                                "id": 12430
                            }
                        ],
                        "account_source": 208
                    }
                ]
            }
        """
        pass

    def add_candidate_to_vacancy(self):
        """POST /account/{account_id}/applicants/{applicant_id}/vacancy

        В теле запроса необходимо передать JSON вида:

            {
                "vacancy": 988,
                "status": 1230,
                "comment": "Привет",
                "files": [
                    {
                        "id": 1382810
                    }
                ],
                "rejection_reason": null
            }
        """
        pass


if __name__ == '__main__':
    pass
