from typing import List, Dict
import logging

from excel_reader import ExcelReader
from candidates import Candidate
from attachment import Attachment
from api_clients.clients import HuntFlowClient


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
                status_text=candidates['statuses'][i],
            )
        )
    return result


def upload_resumes(candidates: List[Candidate], client: HuntFlowClient) -> None:
    """Send resumes using HuntFlow api

    if uploading is successful we store file_id in Candidate.file_id attribute
    """
    for candidate in candidates:
        file_id = client.add_resume_to_hflow(candidate)
        if file_id:
            candidate.files_id = file_id
    return


def add_candidates_to_db(candidates: List[Candidate], client: HuntFlowClient) -> None:
    """Add candidate to database via api and get id"""
    for candidate in candidates:
        candidate_id = client.add_candidate_to_db(candidate)
        if candidate_id:
            candidate.id = candidate_id
    return


def add_candidates_to_vacancy(candidates: List[Candidate], client: HuntFlowClient) -> None:
    for candidate in candidates:
        client.add_candidate_to_vacancy(candidate)
    return


def run() -> None:
    logging.basicConfig(level=logging.DEBUG)
    reader = ExcelReader()
    raw_candidates = reader.read_candidates_from_excel()
    candidates = create_candidates(raw_candidates)
    attachments = Attachment()
    attachments.add_attachment(candidates)

    client = HuntFlowClient()
    upload_resumes(candidates, client)
    add_candidates_to_db(candidates, client)
    add_candidates_to_vacancy(candidates, client)
    return


if __name__ == '__main__':
    run()
