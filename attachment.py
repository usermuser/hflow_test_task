import os
from pathlib import Path, PurePath
from typing import List, Iterable, Tuple, Union, Dict

from candidates import Candidate


class Attachment:
    """Aggregates methods to create attachments"""

    def __init__(self, folder='cv'):
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
                print(files)
                for file in files:
                    key = Path(file.stem)  # prepare key 'Lastname Firstname' for dict
                    fp = Path(file).resolve()  # prepare filepath
                    position = PurePath(address).parts[-1]  # prepare position of candidate
                    result[key] = [fp, position]
        return result

    def _prepare_filename(self, filename: str) -> Tuple[str, Union[str, None]]:
        """Create 'Lastname Firstname' identifier

        For simplicity we assume that filename will consists of only three or two words
        """

        filename = Path(filename).stem  # remove suffix like .pdf
        filename = filename.split(' ')

        if len(filename) == 3:
            lastname_firstname = ' '.join(filename[0:2])
            middlename = filename[2]
            return lastname_firstname, middlename
        elif len(filename) == 2:
            lastname_firstname = ' '.join(filename[0:2])
            middlename = None
            return lastname_firstname, middlename
        else:
            return filename, None

    def _is_tempfile(self, filename: str) -> bool:
        return filename.startswith(('.', '.~', '.~lock'))

    def _remove_tempfiles(self, files) -> List[str]:
        """Create new list without tempfiles"""
        return [file for file in files if self._is_tempfile(file)]

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

        """
        __attachments = self._get_attachments()
        for candidate in candidates:
            if candidate.lastname_firstname in __attachments:
                candidate.fp = __attachments[candidate.lastname_firstname[0]]
                # todo simplify attachments storage structure
        return
