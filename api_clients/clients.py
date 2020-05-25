import json
import logging
import time

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
    ACCOUNT_ID,

)
from candidates import Candidate


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

    @property
    def _set_retries(self) -> int:
        """Check settings for retry strategy"""

        if self.retry:
            return 3 if self.retry_count <= 0 else self.retry_count

        if not self.retry <= 0:
            return 1

    def get(self, url, headers=None, payload=None):
        """GET request with retries"""
        tries = self._set_retries

        while tries > 0:
            try:
                response = requests.get(url, headers=headers, json=payload)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code in self.retry_codes:
                    time.sleep(self.repeat_timeout)
                else:
                    return

            except self.REQUESTS_EXCEPTIONS:
                self.logger.exception('Запрос по адресу %s не удался.' % url)

            except json.decoder.JSONDecodeError:
                self.logger.exception('Запросе по адресу %s не удался: в ответe не JSON: %s' % url, response)

            except Exception:
                self.logger.exception('Внутренняя ошибка!')

            time.sleep(self.retry_timeout)
            tries -= 1
        self.logger.error('Запрос по адресу %s не удался' % url)

        return

    def post(self,
             url,
             headers=None,
             files=None,
             payload=None):
        """Request and response in json format only"""
        tries = self._set_retries
        while tries > 0:
            try:
                response = requests.post(url, headers=headers, files=files, json=payload)

                if response.status_code == 200:
                    print(f'[INFO] response status is: {response.status_code, response.json}')
                    return response.json()
                elif response.status_code in self.retry_codes:
                    print(f'--[INFO] got {response.status_code} going to retry. {response}, tries: {tries}')
                    time.sleep(self.repeat_timeout)
                else:
                    return

            except self.REQUESTS_EXCEPTIONS:
                self.logger.exception('Запрос по адресу %s не удался.' % url)

            except json.decoder.JSONDecodeError:
                self.logger.exception('В ответe не JSON: %s' % response)

            except Exception:
                self.logger.exception('Внутренняя ошибка!')

            time.sleep(self.retry_timeout)
            tries -= 1
        self.logger.error('Запрос по адресу %s не удался' % url)
        return


class HuntFlowClient(BaseClient):
    """Store methods to interact with HuntFlow api"""

    def __init__(self):
        super().__init__()
        self._auth_header = {"Authorization": f"Bearer {TOKEN}"}
        self.account_id = self._get_account_id
        self.appliacant_id = ''  # todo add applicant_id
        self._add_file_url = f'{API_ENDPOINT}account/{self.account_id}/upload'
        self._add_candidate_to_db_url = f'{API_ENDPOINT}account/{self.account_id}/applicants'
        self._add_candidate_to_vacancy_url = f'{API_ENDPOINT}account/{self.account_id}/applicants/{self.applicant_id}'

    @property
    def _get_account_id(self) -> int:
        """Make GET request with credentials and get id from response

        endpoint: /me
        """
        headers = self._auth_header
        url = f'{API_ENDPOINT}accounts'
        response = self.get(url, headers=headers)
        id = response['items'][0]['id']
        return id if id else ACCOUNT_ID

    def get_vacancies(self):
        """GET /account/{account_id}/vacancies

        вернёт список вакансий компании
        """
        pass

    def add_candidate_to_db(self, candidate: Candidate):
        """POST /account/{account_id}/applicants

        last_name and first_name are required fields
        """
        payload = {
            "last_name": candidate.lastname,
            "first_name": candidate.firstname,
            "middle_name": candidate.middlename,
            "position": candidate.position,
            "money": candidate.salary,
        }
        response = self.post(self._add_candidate_to_db_url, headers=self._auth_header, payload=payload)
        if response:
            response = json.loads(response)
            return response['id']

    def add_candidate_to_vacancy(self):
        """POST /account/{account_id}/applicants/{account_id}/vacancy

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

    def add_file_to_hflow(self, candidate: Candidate) -> int:
        """Performs POST request to particular endpoint to add file

        endpoint: /account/{account_id}/upload
        if we want to recognize fields, we can set X-File-Parse: true
        """
        file = {candidate.lastname_firstname: open(candidate.fp, 'rb')}
        payload = {'X-File-Parse': False}
        response = self.post(url=self._add_file_url, headers=self._auth_header, files=file, payload=payload)
        try:
            file_id = response["id"]
        except TypeError:
            file_id = None
        return file_id


if __name__ == '__main__':
    client = HuntFlowClient()
    id = client.account_id
