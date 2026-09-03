from sqlalchemy import ForeignKey, String, INTEGER, FLOAT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from project1.extensions import db

#Analysts should be able to log a press release by specifying a headline, body text, and published date.
class SentimentRecord(db.Model):
    __tablename__ = "sentiment_record"
    sentiment_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sentiment: Mapped[str] = mapped_column(String(100),nullable=False)
    mixed_score: Mapped[float] = mapped_column(FLOAT,nullable=False)
    negative_score: Mapped[float] = mapped_column(FLOAT,nullable=False)
    neutral_score: Mapped[float] = mapped_column(FLOAT,nullable=False)
    positive_score: Mapped[float] = mapped_column(FLOAT,nullable=False)
    press_id: Mapped[int] = mapped_column(INTEGER())

    def __repr__(self):
        return f'Press Name: {self}'
