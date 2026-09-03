""" routes for /api/v1/analysis """

from flask import Blueprint, request, jsonify
from project1.Sentiment_Analysis import service
from project1.Sentiment_Analysis.models import TextAnalysisRequest
from project1.Sentiment_Analysis.service import detect_key_phrases

analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.post("/sentiment")
def sentiment_analysis():
    data = TextAnalysisRequest.model_validate(request.get_json(silent=True) or {})
    return jsonify(service.analyze_sentiment(data.text))

@analysis_bp.get("/sentiment")
def test_key_phrases():
    detect_key_phrases('Seemingly out of nowhere, Nintendo has released to the public an update allowing for local 8 player matches. The update was unexpected but welcomed by the playerbase')
