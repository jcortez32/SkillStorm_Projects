from flask import Blueprint, jsonify
comp_bp = Blueprint('main',__name__) 

#sample routes to test postman
@comp_bp.route('/hel')
def hello():
    return "hello world"

API_PREFIX = '/test'

@comp_bp.get(f"{API_PREFIX}")
def ping():
    return jsonify(status="ok")

@comp_bp.get("")
def get_tickets():
    pass