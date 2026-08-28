#initalizing the different routes our application may receive
from flask import Blueprint, jsonify, request
from project1.Company_Management.store import list_companies, create_company, delete_company, update_company
company_bp = Blueprint('company',__name__) 

#TEST Commands
@company_bp.route('/')
def home():
    return "hello world"

COMPANY_API_PREFIX = '/comp'

#GET Commands
@company_bp.get(f"{COMPANY_API_PREFIX}")
def retrieve_companies():
    companies = list_companies()
    print('company_data:')
    print(companies)
    result = jsonify(count=len(companies), items = [c.model_dump(mode="json") for c in companies])
    return result

#POST Commands
@company_bp.post(f"{COMPANY_API_PREFIX}")
def create_new_company():
    body = request.get_json(silent=True) or {} 
    #body should be company dict
    result = create_company(body)
    print(f"result is equal to:{result}")
    return jsonify(result.model_dump(mode="json")) # setting status code as 201 - CREATED

#DELETE Commands
@company_bp.delete(f"{COMPANY_API_PREFIX}/<ticket_id>")
def delete_new_company(ticket_id):
    if ticket_id is None:
        #raise ApiError(code="not_found", status=400, detail=ticket_id)
        pass
    delete_company(ticket_id)
    return jsonify({"status": "success", "code": 204}) # setting status code as 204 - Deleted

#UPDATE Commands
@company_bp.patch(f"{COMPANY_API_PREFIX}/<company_id>")
def update_a_company(company_id):
    if company_id is None:
        #raise ApiError(code="not_found", status=400, detail=ticket_id)
        pass
    body = request.get_json(silent=True) or {}
    result = update_company(company_id, body)
    return jsonify(result.model_dump(mode="json"))