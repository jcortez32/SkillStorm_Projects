#initalizing the different routes our application may receive
from flask import Blueprint, jsonify, request, render_template
from project1.Company_Management.store import list_companies, create_company, delete_company, update_company, ready_check, get_trend
from project1.responses import ApiError, single_envelope_company
from project1.Press_Release_Management.store import delete_press_via_company
company_bp = Blueprint('company',__name__) 

#TEST Commands
""" confirm flask app is running and willing to accept responses"""
@company_bp.route('/live')
def live():
    return jsonify({"status": "live"}), 200
COMPANY_API_PREFIX = '/companies'

@company_bp.route('/ready')
def ready():
    result = ready_check()
    if result:
        return jsonify({"status": "database ready"}), 200
    else:
        return jsonify({"status": "database unready"}), 503

#GET Commands
'''retrieve list of all companies along with their metadata'''
@company_bp.get(f"{COMPANY_API_PREFIX}")
def retrieve_companies():
    companies = list_companies()
    result = jsonify(count=len(companies), companies = [c.model_dump(mode="json") for c in companies])
    return result
"""show sentiment trend grouped by month"""
@company_bp.get(f"{COMPANY_API_PREFIX}/<company_id>/sentiment-trend")
def get_sentiment_trend(company_id:int):
    result = get_trend(int(company_id))
    if result is False:
        return jsonify(error="Company not found"), 404
    return jsonify(result.model_dump()), 200

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
    body = request.get_json()
    result = False
    if body['company_id'] is not None:
        if int(body['company_id']) == int(company_id):
            #delete any press releases associated with company if they exist
            print('---COMPANY IDS MATCH---')
            delete_press_via_company(company_id)
            result = delete_company(company_id)
        else:
            return jsonify(error="Company IDs do not match"), 400
    else:
        return jsonify({'status': 'malformed request syntax. Body must in form: "company_id": [val]'}), 400
    if result == False:
        return jsonify(error="not found"), 404
    return jsonify({"status": "deleted"}), 204 # setting status code as 204 - Deleted

#PATCH Commands
'''Patch HTTP Request to update a company from the database by specifying ID in url and fields in body'''
@company_bp.patch(f"{COMPANY_API_PREFIX}/<company_id>")
def update_a_company(company_id):
    body = request.get_json(silent=True) or {}
    result = update_company(company_id, body)
    if result == False:
        return jsonify(error="Company not found"), 404
    return jsonify(result.model_dump(mode="json"))