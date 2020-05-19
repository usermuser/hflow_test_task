from excel_reader import ExcelReader
from candidates import Candidate


def create_candidates():
    """Save candidates as list Candidate() objects"""
    result = []
    _candidates_list = ExcelReader.candidates_from_excel()
    for candidate in _candidates_list:
        result.append(
            Candidate(  # we assume that all columns in excel were filled
                position=candidate[0],  # explicit is better than implicit
                fio=candidate[1],
                salary=candidate[2],
                comment=candidate[3],
                status=candidate[4]
            ))
    return result




