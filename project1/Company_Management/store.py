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
    stmt = select(CompanyRecord).order_by(CompanyRecord.id)
    rows = db.session.execute(stmt).scalars()
    result = [Company.model_validate(row) for row in rows]
    return result

def create_company(comp:dict):
    valid_company = CreateCompanyDTO.model_validate(comp)
    record = CompanyRecord(**valid_company.model_dump())
    db.session.add(record)
    db.session.commit()
    return Company.model_validate(record) # setting status code as 201 - CREATED

def delete_company(company_id:int):
    if type(company_id) is str:
        company_id = int(company_id)
    stmt = delete(CompanyRecord).where(CompanyRecord.id==company_id)
    print('--- SQL COMMAND FOR DELETE ---')
    print(stmt)
    print(stmt.compile().params)
    db.session.execute(stmt)
    db.session.commit()
    #return result

#cannot change ticker symbol 
# def update_company(company_id:int):
#     stmt = update(CompanyRecord).where(CompanyRecord.id==company_id).values(name="change")
#     print('--- SQL COMMAND FOR UPDATE ---')
#     print(stmt)
#     db.session.execute(stmt)


def update_company(company_id: int, comp: dict):
    valid_company = UpdateCompanyDTO.model_validate(comp)
    # find the record in the DB
    record = db.session.get(CompanyRecord, company_id)
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
    result = db.session.get(CompanyRecord, company_id)
    return Company.model_validate(record)
    return Ticket.model_validate(record)
    



# UPDATE table_name 
# SET column1 = 'new_value1', column2 = 'new_value2' 
# WHERE condition;


