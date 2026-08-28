from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from project1.extensions import db

#Analysts should be able to log a press release by specifying a headline, body text, and published date.
class PressRecord(db.Model):
    __tablename__ = "press_record"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    headline: Mapped[str] = mapped_column(String(100),nullable=False)
    body_test: Mapped[str] = mapped_column(String(100),nullable=False)
    published_date:Mapped[datetime] = mapped_column(DateTime())

    def __repr__(self):
        return f'Company Name: {self.name}'

    
