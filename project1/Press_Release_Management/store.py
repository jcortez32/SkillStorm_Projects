#where we handle business logic! We do not want business logic in our endpoints.
from pydantic import TypeAdapter
from sqlalchemy import select, delete, update
from project1.Press_Release_Management.db_models import PressRecord
from project1.Press_Release_Management.model_validators import Press
from project1.Company_Management.db_models import CompanyRecord
from project1.Sentiment_Analysis.db_models import SentimentRecord
from project1.extensions import db
from flask import current_app
from datetime import datetime
from typing import Optional, List
from project1.Press_Release_Management.model_validators import CreatePressDTO, UpdatePressDTO

#companies consist of symbol, name, sector and press_release_id
""" returns all press associated with specified company """
def list_press(company_id:int, sentiment:Optional[str], start_date:Optional[datetime], end_date:Optional[datetime]):
    record = db.session.get(CompanyRecord, company_id) 
    if record is None:
        return False 
    stmt = select(PressRecord).join(CompanyRecord, PressRecord.company_id == CompanyRecord.company_id).where(PressRecord.company_id == int(company_id))

    #filter by sentiment 
    if sentiment is not None:
        stmt = stmt.join(SentimentRecord, PressRecord.id == SentimentRecord.press_id).where(SentimentRecord.sentiment == sentiment)

    #filter by start_date and end date
    if start_date is not None:
        stmt = stmt.where(PressRecord.published_date >= start_date)

    if end_date is not None:
        stmt = stmt.where(PressRecord.published_date <= end_date)

    rows = db.session.execute(stmt).scalars()
    result = [Press.model_validate(row) for row in rows]
    return result

def create_press(press:dict,company_id:str):
    valid_company = CreatePressDTO.model_validate(press)
    record = PressRecord(**valid_company.model_dump())
    record.company_id = company_id
    db.session.add(record)
    db.session.commit()
    return Press.model_validate(record) # setting status code as 201 - CREATED

def delete_press(press_id:int) -> bool:
    if type(press_id) is str:
        press_id = int(press_id)
    record = db.session.get(PressRecord, press_id) 
    if record is None:
        return False 
    #delete sentiment records via press_id
    stmt = delete(SentimentRecord).where(SentimentRecord.press_id==press_id)
    db.session.execute(stmt)
    db.session.commit()
    #delete press_record
    stmt = delete(PressRecord).where(PressRecord.id==press_id)
    db.session.execute(stmt)
    db.session.commit()
    return True
    #return result

"""delete all press releases associated with company including sentiment"""
def delete_press_via_company(company_id:int) -> bool:
    print('delete_press_via_company called')
    if type(company_id) is str:
        company_id = int(company_id)
    #identify press ids where company ids match
    stmt = select(PressRecord.id).where(PressRecord.company_id==company_id)
    ids = db.session.execute(stmt).scalars().all()
    #delete sentiment records via press_id
    stmt = delete(SentimentRecord).where(SentimentRecord.press_id.in_(ids))
    db.session.execute(stmt)
    db.session.commit()
    #delete press record where company id matches
    stmt = delete(PressRecord).where(PressRecord.company_id==company_id)
    db.session.execute(stmt)
    db.session.commit()
    return True

"""update press_record via patch. fields can be be empty"""
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