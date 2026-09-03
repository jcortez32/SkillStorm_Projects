from project1.Sentiment_Analysis.models import TextAnalysisRequest
from project1.Sentiment_Analysis import service
from project1.Sentiment_Analysis.db_models import SentimentRecord
from project1.extensions import db
from project1.Press_Release_Management.db_models import PressRecord
from sqlalchemy import update

def create_sentiment(body_text:str, press_id:str):
    #data = TextAnalysisRequest.model_validate(body_text)
    data = service.analyze_sentiment(body_text)
    processed_data = clean_data(data)
    sentiment_record = SentimentRecord(**processed_data)
    print('--- RECORD ---')
    print(sentiment_record.sentiment_id)
    sentiment_record.press_id = int(press_id)
    db.session.add(sentiment_record)
    print('STOP')
    db.session.commit()

def create_phrases(body_text:str, press_id:str):
    data = service.detect_key_phrases(body_text)
    stmt = update(PressRecord).where(PressRecord.id==press_id).values(key_phrases = data)
    db.session.execute(stmt)
    db.session.commit()

def clean_data(data:dict) -> dict:
    scores = data['scores']
    sentiment = data['sentiment']
    processed_data = {
        'sentiment': sentiment,
        'mixed_score': scores['Mixed'],
        'negative_score': scores['Negative'],
        'neutral_score': scores['Neutral'],
        'positive_score': scores['Positive']
    }
    return processed_data
