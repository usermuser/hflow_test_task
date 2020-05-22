"""
В этом файле будет класс, который будет читать данные из эксель файла
"""
import os
from typing import List, Dict

from settings import BASE_DIR
import xlrd

_path = os.getcwd()
excel_path = os.path.join(BASE_DIR, 'excel', 'Тестовая база.xlsx')


class ExcelReader:
    def __init__(self, excel_path=excel_path):
        self.excel_path = excel_path

    def _read_excel(self):
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

    def candidates_from_excel(self):  # todo check each candidate in candidate_from_excel
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

    def _normilize_salary(self, salary):
        # todo change function to work with copy and change it to staticmethod
        """Remove redundant letters like 'рублей' """
        patterns = ['рублей', 'руб', 'р', ' ']
        for pattern in patterns:
            if pattern in str(salary):
                salary = salary.replace(pattern, '')
        return float(salary)


if __name__ == '__main__':
    reader = ExcelReader(excel_path)
    for candidate in reader.candidates_from_excel():
        print(candidate)
    print('\n\n')
    print(reader._candidates_from_excel())
