import os
from sensitive_settings import (
    TOKEN,
    API_ENDPOINT,
    LOGIN,
    PASSWORD,
    ACCOUNT_ID
)

BASE_DIR = os.getcwd()

# RETRY STRATEGY
RETRY_COUNT = 3
RETRY_TIMEOUT = 3
RETRY = True
REPEAT_TIMEOUT = 5
RETRY_CODES = [413, 429, 500, 502, 503, 504]