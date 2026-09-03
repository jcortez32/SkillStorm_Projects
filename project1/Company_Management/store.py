#where we handle business logic! We do not want business logic in our endpoints.
from pydantic import TypeAdapter
from sqlalchemy import select, delete, update
from project1.Company_Management.db_models import CompanyRecord
from project1.Company_Management.model_validators import Company
from project1.extensions import db
from flask import current_app

from project1.Company_Management.model_validators import CreateCompanyDTO, UpdateCompanyDTO

#companies consist of symbol, name, sector and press_release_id 

""" returns all companies """
def list_companies():
    # stmt creates the sql query
    stmt = select(CompanyRecord).order_by(CompanyRecord.company_id)
    rows = db.session.execute(stmt).scalars()
    result = [Company.model_validate(row) for row in rows]
    return result

def create_company(comp:dict):
    valid_company = CreateCompanyDTO.model_validate(comp)
    record = CompanyRecord(**valid_company.model_dump())
    db.session.add(record)
    db.session.commit()
    return Company.model_validate(record) # setting status code as 201 - CREATED

def delete_company(company_id:int) -> bool:
    if type(company_id) is str:
        company_id = int(company_id)
    record = db.session.get(CompanyRecord, company_id) 
    if record is None:
        return False 
    stmt = delete(CompanyRecord).where(CompanyRecord.id==company_id)
    print('--- SQL COMMAND FOR DELETE ---')
    print(stmt)
    db.session.execute(stmt)
    db.session.commit()
    return True

def update_company(company_id: int, comp: dict) -> bool:
    valid_company = UpdateCompanyDTO.model_validate(comp)
    # find the record in the DB
    record = db.session.get(CompanyRecord, company_id)
    if record is None:
        return False    
    # update all the values as needed
    if valid_company.name is not None:
        record.name = valid_company.name
    if valid_company.sector is not None:
        record.sector = valid_company.sector
    db.session.commit()
    # return ticket with new values
    result = db.session.get(CompanyRecord, company_id)
    return Company.model_validate(result)
    return Ticket.model_validate(record)
    



# UPDATE table_name 
# SET column1 = 'new_value1', column2 = 'new_value2' 
# WHERE condition;


