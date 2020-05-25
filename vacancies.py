# todo Consider change class to NamedTuple
class Vacancy:
    def __init__(
            self,
            id,
            position,
            company=None,
            money=int,
            state=str,
            created=str,
            hidden=bool,
            priority=0,
            deadline=None,
            account_division=int,
            applicants_to_hire=1,
            account_vacancy_status_group=None,
            parent=None,
            multiple=False,
            vacancy_request=None
    ):
        self.id = id
        self.position = position  # название вакансии (должности) - Единственное обязательное поле
        self.company = company
        self.money = money
        self.state = state
        self.created = created
        self.hidden = hidden
        self.priority = priority
        self.deadline = deadline
        self.account_division = account_division
        self.applicants_to_hire = applicants_to_hire
        self.account_vacancy_status_group = account_vacancy_status_group
        self.parent = parent
        self.multiple = multiple
        self.vacancy_request = vacancy_request
