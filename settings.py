import os
from sensitive_settings import (
    LOGIN,
    PASSWORD,
    ACCOUNT_ID
)

BASE_DIR = os.getcwd()

# RETRY STRATEGY
RETRY_COUNT = 4
RETRY_TIMEOUT = 2
RETRY = True
REPEAT_TIMEOUT = 2
RETRY_CODES = [413, 429, 500, 502, 503, 504]

# ENDPOINTS
API_ENDPOINT = 'https://dev-100-api.huntflow.ru/'
