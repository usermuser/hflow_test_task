from typing import List, Dict

from excel_reader import ExcelReader
from candidates import Candidate
from attachment import Attachment


def create_candidates(candidates: Dict):
    result = []
    for i in range(len(candidates['fios'])):
        result.append(
            Candidate(
                position=candidates['positions'][i],
                fio=candidates['fios'][i],
                salary=candidates['salary_requests'][i],
                comment=candidates['comments'][i],
                status=candidates['statuses'][i],
            )
        )
    print(f'[INFO] result is: {result}')
    return result


if __name__ == '__main__':
    reader = ExcelReader()
    candidates_from_excel = reader.get_candidates_from_excel()
    candidates = create_candidates(candidates_from_excel)
    attachments = Attachment()
    attachments.add_attachment(candidates)

    for c in candidates:
        print(c.fp)
