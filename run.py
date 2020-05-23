from typing import List, Dict

from excel_reader import ExcelReader
from candidates import Candidate
from attachment import Attachment


def create_candidates(candidates: Dict) -> List[Candidate]:
    """Converts candidates records from dict to objects"""
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
    return result


if __name__ == '__main__':
    reader = ExcelReader()
    raw_candidates = reader.get_candidates_from_excel()
    candidates = create_candidates(raw_candidates)
    attachments = Attachment()
    attachments.add_attachment(candidates)
