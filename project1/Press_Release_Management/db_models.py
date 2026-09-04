from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, Text, DateTime, INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship
from project1.extensions import db
from sqlalchemy.dialects.postgresql import JSONB

#Analysts should be able to log a press release by specifying a headline, body text, and published date.
class PressRecord(db.Model):
    __tablename__ = "press_record"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    headline: Mapped[str] = mapped_column(String(100),nullable=False)
    body_test: Mapped[str] = mapped_column(String(5000),nullable=False)
    published_date:Mapped[datetime] = mapped_column(DateTime()) #eg. 2026-08-28 
    company_id: Mapped[int] = mapped_column(INTEGER())
    key_phrases: Mapped[dict] = mapped_column(JSONB(), nullable=True)
    def __repr__(self):
        return f'Press Name: {self.id}'

    
