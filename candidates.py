"""
В этом файле будет базовый класс BaseCandidate и наследник Candidate,
экземпляры класса Candidate мы будем использовать для хранения данных из эксель файла о каждом кандидате.
"""


class BaseCandidate:

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
        self.__parse_fio()

    def __parse_fio(self):
        """Create separated attributes firstname, last name (also middlename if provided"""

        __fio_as_list = self.fio.split(' ')
        if len(__fio_as_list) == 3:
            self.lastname, self.firstname, self.middlename = __fio_as_list
        elif len(__fio_as_list) == 2:
            self.lastname, self.firstname = __fio_as_list
        return

    @property
    def lastname_firstname(self):
        return ' '.join([self.lastname, self.firstname])

    def __repr__(self):
        return self.lastname_firstname


class Candidate(BaseCandidate):
    pass
