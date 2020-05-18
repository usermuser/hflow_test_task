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

    def parse_excel(self):
        with open(excel_path, encoding='utf-8', 'r') as excel:

