from excel_reader import ExcelReader
from candidates import Candidate
from attachment import Attachment


def save_candidates():
    """Read excel file with candidates information and store in a list"""
    _result = []
    _read = ExcelReader()
    _candidates_list = _read.candidates_from_excel()
    for candidate in _candidates_list:
        _result.append(
            Candidate(  # we assume that all columns in excel were filled
                position=candidate[0],
                fio=candidate[1],
                salary=candidate[2],
                comment=candidate[3],
                status=candidate[4]
            ))
    return _result


if __name__ == '__main__':
    candidates = save_candidates()
    attachments = Attachment()
    attachments.add_attachment(candidates)
    2 + 2
