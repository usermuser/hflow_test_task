import os
from pathlib import Path, PurePath
from typing import List, Iterable, Tuple, Union, Dict

from candidates import Candidate
from utils.utils import EXCEL_FOLDER

UNDESIRABLE_SYMBOLS = (("й", "й"),)


class Attachment:
    """Aggregates methods to create attachments"""

    def __init__(self, folder=EXCEL_FOLDER):
        self.folder = folder

    def _get_attachments(self) -> Dict:
        """Scan folder and save paths

        :returns Dict
        fp - filepath

        Dict = {
                    'Lastname Name': ['fp', 'profession'],
                    'Lastname2 Name2': ['fp2', 'profession2'],
                    ...
                }
        """
        result = {}
        for address, dirs, files in os.walk(self.folder):
            if files:
                files = self._remove_tempfiles(files)
                for file in files:
                    lastname_firstname, middlename = self._prepare_filename(file)
                    key = lastname_firstname
                    fp = str(Path().resolve().joinpath(address, file))
                    position = PurePath(address).parts[-1]  # prepare position of candidate
                    result[key] = [fp, position, middlename]
        return result

    def _prepare_filename(self, filename_as_list: str) -> Tuple[str, Union[str, None]]:
        """Create 'Lastname Firstname' identifier

        For simplicity we assume that filename_as_list will consists of only three or two words
        """

        raw_filename = Path(filename_as_list).stem  # remove suffix like .pdf
        filename = self._replace_undesirable_symbol(raw_filename)
        filename_as_list = filename.split(' ')

        if len(filename_as_list) == 3:
            lastname_firstname = ' '.join(filename_as_list[0:2])
            middlename = filename_as_list[2]
            return lastname_firstname, middlename
        elif len(filename_as_list) == 2:
            lastname_firstname = ' '.join(filename_as_list[0:2])
            middlename = None
            return lastname_firstname, middlename
        else:
            return filename_as_list, None

    @staticmethod
    def _replace_undesirable_symbol(text: str) -> str:
        result_text = str
        for bad_symbol, good_symbol in UNDESIRABLE_SYMBOLS:
            result_text = text.replace(bad_symbol, good_symbol)
        return result_text

    @staticmethod
    def _is_tempfile(filename: str) -> bool:
        return filename.startswith(('.', '.~', '.~lock'))

    def _remove_tempfiles(self, files) -> List[str]:
        """Create new list without tempfiles"""
        return [file for file in files if not self._is_tempfile(file)]

    def add_attachment(self, candidates: Iterable[Candidate]) -> None:
        """Add path to cv for every candidate

        If we have cv file with same 'Lastname Firstname' as in excel file
        we add path to to this cv
        Example:
            in excel file we have entry like this: 'Иванов Иван',
            and also we have 'Иванов Иван.pdf' file
            this method will add path of this file to candidate object.

        Also for future improvements we keep folder name where 'Иванов Иван.pdf'
        file stored, because folder name equals position column in excel file
        Example:
            Должность:                 folder name:
            Менеджер по продажам       Менеджер по продажам

        _attachments is a dict with 'Lastname Firstname' as key and [fp, position, middlename] as value
            [0] -> fp, [1] -> position, [2] -> middlename (Can be None)
        """
        _attachments = self._get_attachments()
        for candidate in candidates:
            if candidate.lastname_firstname in _attachments:
                candidate.fp = _attachments[candidate.lastname_firstname][0]
        return
