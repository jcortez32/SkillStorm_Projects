#initalizing the different routes our application may receive
from flask import Blueprint, jsonify
main_bp = Blueprint('main',__name__) 

#GET Commands
@main_bp.route('/')
def home():
    return "hello world"

COMPANY_API_PREFIX = '/comp'

@main_bp.get(f"{COMPANY_API_PREFIX}")
def ping():
    return jsonify(status="ok")

#POST Commands
@main_bp.post('')
def create_new_company():
    pass