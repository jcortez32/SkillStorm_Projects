""" calling AWS Comprehend with boto3 """ 

import json
from project1.Sentiment_Analysis.aws import get_client
from botocore.exceptions import ClientError


def analyze_sentiment(text: str) -> dict:
    """ use Amazon comprehend to determine overall tone of text """
    try:
        response = get_client("comprehend").detect_sentiment(
            Text=text,
            LanguageCode="en"
        )
        return {
            "sentiment": response["Sentiment"],
            # rounding the confidence value to 3 decimal places
            "scores": {k : round(v, 3) for k, v in response["SentimentScore"].items()}
        }
    except(ClientError) as e:
        return {
            "sentiment": "UNKNOWN",
            "scores": {
                "Positive": 0.0,
                "Negative": 0.0,
                "Neutral": 1.0,
                "Mixed": 0.0
            }
        } 

def detect_key_phrases(text: str):
    response = get_client("comprehend").detect_key_phrases(
        Text=text,
        LanguageCode="en"
    )
    return response['KeyPhrases']
