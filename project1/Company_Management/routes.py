#initalizing the different routes our application may receive
from flask import Blueprint, jsonify, request
from project1.Company_Management.store import list_companies, create_company, delete_company, update_company
from project1.responses import ApiError, single_envelope_company
company_bp = Blueprint('company',__name__) 

#TEST Commands
@company_bp.route('/live')
def home():
    return "hello world"

COMPANY_API_PREFIX = '/comp'

#GET Commands
'''retrieve list of all companies along with their metadata'''
@company_bp.get(f"{COMPANY_API_PREFIX}")
def retrieve_companies():
    companies = list_companies()
    result = jsonify(count=len(companies), items = [c.model_dump(mode="json") for c in companies])
    return result

#POST Commands
'''Create company record to commit to database'''
@company_bp.post(f"{COMPANY_API_PREFIX}")
def create_new_company():
    body = request.get_json()
    #check if body is missing
    if not body:
        return jsonify(error="missing payload"), 400
    #check if body is missing any required fields
    if 'symbol' not in body:
        return jsonify(error="missing 'symbol in payload"), 422
    elif 'name' not in body:
        return jsonify(error="missing 'name' in payload"), 422
    elif 'sector' not in body:
        return jsonify(error="missing 'sector' in payload"), 422 
        
    result = create_company(body)
    return jsonify(result.model_dump(mode="json")), 201 # setting status code as 201 - CREATED

#DELETE Commands
'''delete a company from the database by specifying ID'''
@company_bp.delete(f"{COMPANY_API_PREFIX}/<company_id>")
def delete_new_company(company_id):
    result = delete_company(company_id)
    if result == False:
        return jsonify(error="not found"), 404
    return jsonify({"status": "deleted", "code": 204}) # setting status code as 204 - Deleted

#PATCH Commands
'''Patch HTTP Request to update a company from the database by specifying ID in url and fields in body'''
@company_bp.patch(f"{COMPANY_API_PREFIX}/<company_id>")
def update_a_company(company_id):
    body = request.get_json(silent=True) or {}
    result = update_company(company_id, body)
    if result == False:
        return jsonify(error="Company not found"), 404
    return jsonify(result.model_dump(mode="json"))