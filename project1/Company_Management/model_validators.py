from pydantic import BaseModel, ConfigDict
from sqlalchemy import select, text
from datetime import datetime
from typing import List
class Company(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    company_id:int 
    symbol:str
    name:str
    sector:str

class Company_and_press(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    company_id:int 
    symbol:str
    name:str
    sector:str
    press_release_count:int = None

class CreateCompanyDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")
    symbol:str
    name:str
    sector:str

class UpdateCompanyDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name:str|None = None
    sector:str|None = None

class SentimentTrendPoint(BaseModel):
    period: str 
    total_releases: int
    avg_positive: float
    avg_negative: float
    avg_neutral: float
    avg_mixed: float
    dominant_sentiment: str

class SentimentTrendResponse(BaseModel):
    company_id: int
    trend: List[SentimentTrendPoint]