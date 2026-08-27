#where we handle business logic! We do not want business logic in our endpoints.
from pydantic import TypeAdapter
from sqlalchemy import select, text
from db_models import CompanyRecord
from model_validators import Company
from src.extensions import db
from flask import current_app

from src.model_validators import CreateCompanyDTO

#companies consist of symbol, name, sector and press_release_id 

""" returns all companies """
def list_companies():
    # stmt creates the sql query
    stmt = select(CompanyRecord).order_by(CompanyRecord.id)
    rows = db.session.execute(stmt).scalars()
    result = [Company.model_validate(row) for row in rows]
    return result

def create_company(comp:dict):
    valid_company = CreateCompanyDTO.model_validate(comp)
    record = CompanyRecord(**valid_company.model_dump)
    db.session.add(record)
    db.session.commit()
    return Company.model_validate