from flask import jsonify
from project1.Press_Release_Management.db_models import PressRecord
from project1.Company_Management.db_models import CompanyRecord

class ApiError(Exception):
    def __init__(self, code: str, status: int, detail: str | None = None):

        super().__init__(detail or code)
        self.code = code
        self.status = status
        self.detail = detail

def single_envelope_press(ticket: PressRecord):
    return jsonify(PressRecord.model_dump(mode="json"))

def single_envelope_company(ticket: CompanyRecord):
    return jsonify(CompanyRecord.model_dump(mode="json"))

def error_response(code: str, status: int, detail: str | None = None):
    return jsonify(error=code, detail=detail), status