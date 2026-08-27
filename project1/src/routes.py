#initalizing the different routes our application may receive
from flask import Blueprint, jsonify
from store import list_companies
main_bp = Blueprint('main',__name__) 

#GET Commands
@main_bp.route('/')
def home():
    return "hello world"

COMPANY_API_PREFIX = '/comp'

@main_bp.get(f"{COMPANY_API_PREFIX}")
def ping():
    companies = list_companies()
    print('company_data:')
    print(companies)
    result = jsonify(count=len(companies), items = [c.model_dump(mode="json") for c in companies])
    return result

#POST Commands
@main_bp.post('/')
def create_new_company():
    return jsonify(status="ok")