#where we handle business logic! We do not want business logic in our endpoints.
from pydantic import TypeAdapter
from sqlalchemy import select, delete, update, func, text
from project1.Company_Management.db_models import CompanyRecord
from project1.Press_Release_Management.db_models import PressRecord
from project1.Company_Management.model_validators import Company, Company_and_press
from project1.extensions import db
from flask import current_app
from typing import Literal
from project1.Company_Management.model_validators import CreateCompanyDTO, UpdateCompanyDTO, SentimentTrendPoint,SentimentTrendResponse
from project1.Sentiment_Analysis.db_models import SentimentRecord
#lightweight ping check
def ready_check():
    try:
        db.session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        return False
    
""" returns all companies """
def list_companies():
    #stmt = select(CompanyRecord).order_by(CompanyRecord.company_id)
    stmt2 = select(CompanyRecord, func.count(PressRecord.company_id).label('press_count')).select_from(CompanyRecord).outerjoin(PressRecord, CompanyRecord.company_id == PressRecord.company_id).group_by(CompanyRecord.company_id)
    rows = db.session.execute(stmt2).all()
    press_counts = [row.press_count for row in rows]
    companies = [Company_and_press.model_validate(row.CompanyRecord) for row in rows]
    for index, company in enumerate(companies):
        company.press_release_count = press_counts[index]
    return companies

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
    stmt = delete(CompanyRecord).where(CompanyRecord.company_id==company_id)
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

def get_trend(company_id: int):
    company = db.session.get(CompanyRecord, company_id)
    if not company:
        return False

    period_col = func.date_trunc('month', PressRecord.published_date).label("period")
    stmt = (
        select(period_col,func.count(PressRecord.id).label("total_releases"),func.avg(SentimentRecord.positive_score).label("avg_positive"),func.avg(SentimentRecord.negative_score).label("avg_negative"),func.avg(SentimentRecord.neutral_score).label("avg_neutral"),func.avg(SentimentRecord.mixed_score).label("avg_mixed"))
        .join(SentimentRecord, PressRecord.id == SentimentRecord.press_id).where(PressRecord.company_id == company_id)
        .group_by(period_col).order_by(period_col.asc())
    )
    rows = db.session.execute(stmt).all()
    trend_points = []
    for row in rows:
        # Determine dominant sentiment for the bucket based on aggregated scores
        scores = {
            "POSITIVE": row.avg_positive,
            "NEGATIVE": row.avg_negative,
            "NEUTRAL": row.avg_neutral,
            "MIXED": row.avg_mixed
        }
        dominant = max(scores, key=scores.get)
        period_dt = row.period
        period_str = period_dt.strftime("%Y-%m")
        trend_points.append(
            SentimentTrendPoint(
                period=period_str,
                total_releases=row.total_releases,
                avg_positive=round(row.avg_positive, 3),
                avg_negative=round(row.avg_negative, 3),
                avg_neutral=round(row.avg_neutral, 3),
                avg_mixed=round(row.avg_mixed, 3),
                dominant_sentiment=dominant
             )
        )
    return SentimentTrendResponse(company_id=company_id,trend=trend_points)