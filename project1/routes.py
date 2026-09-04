#initalizing the different routes our application may receive
from flask import Blueprint, render_template, request, jsonify
from project1.Company_Management.store import create_company, update_company
from project1.Press_Release_Management.store import create_press
from project1.Sentiment_Analysis.store import create_phrases,create_sentiment
main_bp = Blueprint('main',__name__) 

#TEST Commands
@main_bp.route('/')
def home():
    return render_template("index.html")


#POST Command for Company
'''Create company record to commit to database'''
@main_bp.post('/web-company')
def create_new_company_via_web():
    print('create_new_company_via_web called')
    symbol = request.form.get("symbol")
    name = request.form.get("name")
    sector = request.form.get("sector")
    body = {'symbol':symbol, 'name': name, 'sector': sector}
    result = create_company(body)
    return jsonify(result.model_dump(mode="json")), 201 # setting status code as 201 - CREATED



#POST Command for Press
'''Create company record to commit to database'''
@main_bp.post('/web-press_release')
def create_new_press_via_web():
    print('create_new_press_via_web called')
    headline = request.form.get("headl")
    text = request.form.get("body")
    date = request.form.get("pdate")
    body = {'headline':headline, 'body_test': text, 'published_date': date}
    id = request.form.get("compID")
    result = create_press(body,id)
    create_sentiment(body['body_test'], result.id)
    create_phrases(body['body_test'], result.id)
    return jsonify(result.model_dump(mode="json")), 201 # setting status code as 201 - CREATED
