#where we handle business logic! We do not want business logic in our endpoints.
from pydantic import TypeAdapter
from sqlalchemy import select, delete, update
from project1.Press_Release_Management.db_models import PressRecord
from project1.Press_Release_Management.model_validators import Press
from project1.extensions import db
from flask import current_app

from project1.Press_Release_Management.model_validators import CreatePressDTO, UpdatePressDTO

#companies consist of symbol, name, sector and press_release_id 

""" returns all companies """
def list_press():
    # stmt creates the sql query
    stmt = select(PressRecord).order_by(PressRecord.id)
    rows = db.session.execute(stmt).scalars()
    result = [Press.model_validate(row) for row in rows]
    return result

def create_press(comp:dict):
    valid_company = CreatePressDTO.model_validate(comp)
    record = PressRecord(**valid_company.model_dump())
    db.session.add(record)
    db.session.commit()
    return Press.model_validate(record) # setting status code as 201 - CREATED

def delete_press(company_id:int):
    if type(company_id) is str:
        company_id = int(company_id)
    stmt = delete(PressRecord).where(PressRecord.id==company_id)
    print('--- SQL COMMAND FOR DELETE ---')
    print(stmt)
    print(stmt.compile().params)
    db.session.execute(stmt)
    db.session.commit()
    #return result

def update_press(company_id: int, comp: dict):
    valid_company = UpdatePressDTO.model_validate(comp)
    # find the record in the DB
    record = db.session.get(PressRecord, company_id)
    if record is None:
        return None     # return none if no record found
    # update all the values
    if valid_company.name is not None:
        record.name = valid_company.name
    if valid_company.sector is not None:
        record.sector = valid_company.sector
    # commit the updated values
    db.session.commit()
    # return ticket with new values
    result = db.session.get(PressRecord, company_id)
    return Press.model_validate(record)
    return Ticket.model_validate(record)
    



# UPDATE table_name 
# SET column1 = 'new_value1', column2 = 'new_value2' 
# WHERE condition;


