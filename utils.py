import os
import argparse
from typing import Tuple

from sensitive_settings import (
    DEFAULT_TOKEN,

)


def parse_command_line() -> Tuple[str, str]:
    """Extract token or path to folder with excel file if provided"""
    excel_folder = os.path.join(os.getcwd(), 'excel')

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store', dest='token')
    parser.add_argument('-p', action='store', dest='excel_folder')
    args = parser.parse_args()
    token = args.token if args.token else DEFAULT_TOKEN
    excel_folder = check_path(args, excel_folder)
    print(f'token is: {token}, and folder is: {excel_folder}')
    return token, excel_folder


def check_path(args: argparse.Namespace, path: str) -> str:
    """Check path provided via command line or default path

    todo handle situation when path provided via command line is wrong
    todo handle situation when default path is wrong
    """
    if args.excel_folder and os.path.isdir(args.excel_folder):
        return args.excel_folder
    else:
        return path
