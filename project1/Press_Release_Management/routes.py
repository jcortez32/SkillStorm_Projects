#initalizing the different routes our application may receive
from flask import Blueprint, jsonify, request
from project1.Press_Release_Management.store import list_press,create_press,update_press,delete_press
from project1.responses import ApiError, single_envelope_press
from project1.Sentiment_Analysis.service import analyze_sentiment
from project1.Sentiment_Analysis.store import create_sentiment, create_phrases
press_bp = Blueprint('press',__name__) 

PRESS_API_PREFIX = '/press'

#GET Commands
@press_bp.get(f"{PRESS_API_PREFIX}/<company_id>")
def retrieve_press(company_id):
    press_files = list_press(company_id)
    if press_files == False:
        return jsonify(error="Company not found"), 404
    result = jsonify(count=len(press_files), items = [p.model_dump(mode="json") for p in press_files])
    return result

#POST Commands
@press_bp.post(f"{PRESS_API_PREFIX}/<company_id>")
def create_new_press(company_id):
    body = request.get_json(silent=True) or {} 
    if not body:
        return jsonify(error="missing payload"), 400
    #check if body is missing any required fields
    if 'headline' not in body:
        return jsonify(error="missing 'headline' in payload"), 422
    elif 'body_test' not in body:
        return jsonify(error="missing 'body_test' in payload"), 422
    elif 'published_date' not in body:
        return jsonify(error="missing 'published_date' in payload"), 422 
    result = create_press(body,company_id)
    create_sentiment(body['body_test'], result.id)
    create_phrases(body['body_test'], result.id)
    print(f"result is equal to:{result}")
    return jsonify(result.model_dump(mode="json")),201 # setting status code as 201 - CREATED

#DELETE Commands
@press_bp.delete(f"{PRESS_API_PREFIX}/<press_id>")
def delete_new_press(press_id):
    result = delete_press(press_id)
    if result == False:
        return jsonify(error="Press Release not found"), 404
    return jsonify({"status": "success", "code": 204}) # setting status code as 204 - Deleted

#UPDATE Commands
@press_bp.patch(f"{PRESS_API_PREFIX}/<press_id>")
def update_a_press(press_id):
    body = request.get_json(silent=True) or {}
    result = update_press(press_id, body)
    if result == False:
        return jsonify(error="Press Release not found"), 404
    return jsonify(result.model_dump(mode="json"))