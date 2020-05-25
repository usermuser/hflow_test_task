"""
В этом файле будет базовый класс BaseCandidate и наследник Candidate,
экземпляры класса Candidate мы будем использовать для хранения данных из эксель файла о каждом кандидате.
"""
from vacancies import Vacancy


class BaseCandidate:

    def __init__(self, position, fio, salary='', comment='', status_text='', fp=''):
        self.position = position
        self.fio = fio
        self.salary = salary
        self.comment = comment
        self.status_text = status_text
        self.fp = fp
        self.firstname = ''
        self.middlename = ''
        self.lastname = ''
        self._parse_fio()
        self.files_id = []
        self.id = int
        self.rejection_reason = ''

    def _parse_fio(self):
        """Create separated attributes firstname, last name (also middlename if provided"""

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
        return self.lastname_firstname


class Candidate(BaseCandidate):

    @property
    def status_id(self) -> int:
        """Temporary hardcoded method"""
        _statuses = {
            'Отправлено письмо': 42,
            'Интервью с HR': 44,
            'Выставлен оффер': 46,
            'Отказ': 50
        }
        # todo add errors handling
        return _statuses[self.status_text]

    def is_suitable_for(self, vacancy: Vacancy) -> bool:
        """Check if candidate is suitable for vacancy"""
        return vacancy.position == self.position
