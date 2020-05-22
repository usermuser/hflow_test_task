"""
В этом файле будет класс, который будет читать данные из эксель файла
"""
import os
from settings import BASE_DIR
from candidates import Candidate
import xlrd

_path = os.getcwd()
excel_path = os.path.join(BASE_DIR, 'excel', 'Тестовая база.xlsx')


class ExcelReader():
    def __init__(self, excel_path):
        self.excel_path = excel_path

    def candidates_from_excel(self):  # todo check each candidate in candidate_from_excel
        """Save excel data as list of lists"""
        wb = xlrd.open_workbook(self.excel_path)
        sheet = wb.sheet_by_index(0)  # for simplicity we assume that we have only one sheet always
        _number_of_rows = sheet.nrows
        result = []
        for row in range(1, _number_of_rows):  # run over all rows except first one
            __row = []  # todo explain this line and this piece of code
            for value in sheet.row_values(row):
                __row.append(value)
            result.append(__row)
        return result


if __name__ == '__main__':
    reader = ExcelReader(excel_path)
for candidate in reader.candidates_from_excel():
    print(candidate)
