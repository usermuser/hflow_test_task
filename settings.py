import os
import utils
from sensitive_settings import ACCOUNT_ID

# RETRY STRATEGY
RETRY_COUNT = 4
RETRY_TIMEOUT = 2
RETRY = True
REPEAT_TIMEOUT = 2
RETRY_CODES = [413, 429, 500, 502, 503, 504]

# ENDPOINTS
API_ENDPOINT = 'https://dev-100-api.huntflow.ru/'

FILENAME = 'Тестовая база.xlsx'
TOKEN, EXCEL_FOLDER = utils.parse_command_line()
EXCEL_FILE = os.path.join(EXCEL_FOLDER, FILENAME)
