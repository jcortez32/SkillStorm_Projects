from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from project1.extensions import db

#Analysts should be able to add a tracked company by specifying its ticker symbol, name, and sector
class CompanyRecord(db.Model):
    __tablename__ = "company_record"
    company_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(100),nullable=False)
    name: Mapped[str] = mapped_column(String(100),nullable=False)
    sector: Mapped[str] = mapped_column(String(100),nullable=False)

    #store company metadata
    #created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def __repr__(self):
        return f'Company Name: {self.name}'

    
