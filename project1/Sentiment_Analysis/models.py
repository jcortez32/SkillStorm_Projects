from pydantic import BaseModel, ConfigDict, Field

class TextAnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # AWS Comprehend has a 5000 character limit
    text: str = Field(min_length=1, max_length=5000)