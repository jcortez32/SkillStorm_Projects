#where we handle business logic! We do not want business logic in our endpoints.
from pydantic import TypeAdapter
from sqlalchemy import select, text
from db_models import CompanyRecord
from model_validators import Company
from extensions import db

from src.model_validators import CreateCompanyDTO

#companies consist of symbol, name, sector and press_release_id 

""" returns all companies """
def list_companies():
    # stmt creates the sql query
    #stmt = select(TicketRecord).order_by(TicketRecord.id)
    pass

def create_company(comp:dict):
    valid_company = CreateCompanyDTO.model_validate(comp)
    record = CompanyRecord(**valid_company.model_dump)
    db.session.add(record)
    db.session.commit()
    return Company.model_validate