"""
В этом файле будет базовый класс BaseCandidate и наследник Candidate,
экземпляры класса Candidate мы будем использовать для хранения данных из эксель файла о каждом кандидате.
"""


class BaseCandidate:
    firstname: str

    def __init__(self, position, fio, salary='', comment='', status='', fp=''):
        self.position = position
        self.fio = fio
        self.salary = salary
        self.comment = comment
        self.status = status
        self.fp = fp
        self.firstname = ''
        self.middlename = ''
        self.lastname = ''
        self.parse_fio()

    def parse_fio(self):
        _fio_as_list = self.fio.split(' ')
        if len(_fio_as_list) == 3:
            self.lastname, self.firstname, self.middlename = _fio_as_list
        elif len(_fio_as_list) == 2:
            self.lastname, self.firstname = _fio_as_list
        return

    @property
    def lastname_firstname(self):
        return ' '.join([self.lastname, self.firstname])

    def __repr__(self):
        pass
