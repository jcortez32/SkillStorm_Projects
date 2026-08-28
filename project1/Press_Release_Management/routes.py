#initalizing the different routes our application may receive
from flask import Blueprint, jsonify, request
from project1.Press_Release_Management.store import list_press,create_press,update_press,delete_press
press_bp = Blueprint('press',__name__) 

PRESS_API_PREFIX = '/press'

#GET Commands
@press_bp.get(f"{PRESS_API_PREFIX}")
def retrieve_press():
    #must update so that it only lists for a specific company
    press_files = list_press()
    result = jsonify(count=len(press_files), items = [p.model_dump(mode="json") for p in press_files])
    return result

#POST Commands
@press_bp.post(f"{PRESS_API_PREFIX}")
def create_new_press():
    body = request.get_json(silent=True) or {} 
    #body should be press dict
    result = create_press(body)
    print(f"result is equal to:{result}")
    return jsonify(result.model_dump(mode="json")) # setting status code as 201 - CREATED

#DELETE Commands
@press_bp.delete(f"{PRESS_API_PREFIX}/<press_id>")
def delete_new_press(press_id):
    if press_id is None:
        #raise ApiError(code="not_found", status=400, detail=ticket_id)
        pass
    delete_press(press_id)
    return jsonify({"status": "success", "code": 204}) # setting status code as 204 - Deleted

#UPDATE Commands
@press_bp.patch(f"{PRESS_API_PREFIX}/<press_id>")
def update_a_company(press_id):
    if press_id is None:
        #raise ApiError(code="not_found", status=400, detail=ticket_id)
        pass
    body = request.get_json(silent=True) or {}
    result = update_press(press_id, body)
    return jsonify(result.model_dump(mode="json"))