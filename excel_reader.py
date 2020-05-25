"""
В этом файле будет класс, который будет читать данные из эксель файла
"""
import os
from typing import List, Dict
import xlrd

from settings import EXCEL_FILE


class ExcelReader:
    def __init__(self, excel_path=EXCEL_FILE):
        self.excel_path = excel_path

    def _read_excel(self) -> List:
        """Read excel file except headers

        for simplicity we assume that we have only one sheet always
        """
        wb = xlrd.open_workbook(self.excel_path)
        sheet = wb.sheet_by_index(0)
        _number_of_rows = sheet.nrows
        _data = []
        _columns = sheet.ncols
        for column in range(_columns):
            column_data = sheet.col_values(column, start_rowx=1)
            _data.append(column_data)
        return _data

    def read_candidates_from_excel(self) -> Dict:  # todo check each candidate in candidate_from_excel
        """Save excel data """
        excel_data: List
        excel_data = self._read_excel()
        candidates = {
            'positions': excel_data[0],
            'fios': excel_data[1],
            'salary_requests': excel_data[2],
            'comments': excel_data[3],
            'statuses': excel_data[4]
        }
        # remove redundant whitespaces from 'ФИО' column
        # '  Иванов Иван   ' -> 'Иванов Иван'
        candidates['fios'] = list(map(str.strip, candidates['fios']))
        candidates['salary_requests'] = list(map(self._normilize_salary, candidates['salary_requests']))

        return candidates

    @staticmethod
    def _normilize_salary(salary):
        # todo change function to work with copy and change it to staticmethod
        """Remove redundant letters like 'рублей' """
        patterns = ['рублей', 'руб', 'р', ' ']
        for pattern in patterns:
            if pattern in str(salary):
                salary = salary.replace(pattern, '')
        return float(salary)
