#where we handle business logic! We do not want business logic in our endpoints.
from pydantic import TypeAdapter
from sqlalchemy import select, delete, update
from project1.Press_Release_Management.db_models import PressRecord
from project1.Press_Release_Management.model_validators import Press
from project1.Company_Management.db_models import CompanyRecord
from project1.extensions import db
from flask import current_app

from project1.Press_Release_Management.model_validators import CreatePressDTO, UpdatePressDTO

#companies consist of symbol, name, sector and press_release_id 

""" returns all press associated with specified company """
# SELECT press_record.headline, press_record.body_test, published_date
# FROM press_record 
# JOIN company_record 
# ON company_record.company_id = press_record.company_id
# WHERE press_record.company_id = 2
def list_press(company_id:int):
    record = db.session.get(CompanyRecord, company_id) 
    if record is None:
        return False 
    stmt = select(PressRecord).join(CompanyRecord, PressRecord.company_id == CompanyRecord.company_id).where(PressRecord.company_id == int(company_id))
    print("--- GET PRESS QUERY ---")
    print(stmt)
    rows = db.session.execute(stmt).scalars()
    result = [Press.model_validate(row) for row in rows]
    return result

def create_press(press:dict,company_id:str):
    valid_company = CreatePressDTO.model_validate(press)
    record = PressRecord(**valid_company.model_dump())
    record.company_id = company_id
    db.session.add(record)
    print('--- SQL RECORD ---')
    print(record.company_id)
    db.session.commit()
    return Press.model_validate(record) # setting status code as 201 - CREATED

def delete_press(press_id:int) -> bool:
    if type(press_id) is str:
        press_id = int(press_id)
    record = db.session.get(PressRecord, press_id) 
    if record is None:
        return False 
    stmt = delete(PressRecord).where(PressRecord.id==press_id)
    print('--- SQL COMMAND FOR DELETE ---')
    print(stmt)
    print(stmt.compile().params)
    db.session.execute(stmt)
    db.session.commit()
    return True
    #return result

def update_press(press_id: int, body: dict):
    valid_press = UpdatePressDTO.model_validate(body)
    # find the record in the DB
    record = db.session.get(PressRecord, press_id)
    if record is None:
        return False     # return none if no record found
    # update all the values
    if valid_press.headline is not None:
        record.headline = valid_press.headline
    if valid_press.body_test is not None:
        record.body_test = valid_press.body_test
    if valid_press.published_date is not None:
        record.published_date = valid_press.published_date
    # commit the updated values
    db.session.commit()
    # return ticket with new values
    return Press.model_validate(record)
    return Ticket.model_validate(record)
    



# UPDATE table_name 
# SET column1 = 'new_value1', column2 = 'new_value2' 
# WHERE condition;


