import argparse
from sensitive_settings import (
    DEFAULT_TOKEN,

)


def set_token():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store', dest='token')
    parser.add_argument('-p', action='store', dest='excel_folder')
    args = parser.parse_args()
    token = args.token if args.token else TOKEN
    excel_folder = args.excel_folder if args.excel_folder else 'cv'
    return token, excel_folder


TOKEN, EXCEL_FOLDER = set_token()