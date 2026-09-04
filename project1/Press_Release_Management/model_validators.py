from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select, text
from datetime import datetime
from typing import Optional, List, Dict, Any
class Press(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int 
    headline:str
    body_test:str
    published_date:datetime
    company_id:int
    key_phrases: Optional[List[str]] = None
    sentiment: Optional[str] = None


class CreatePressDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")
    headline:str = Field(min_length=10) 
    body_test:str = Field(min_length=20, max_length=5000)
    published_date:str

class UpdatePressDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")
    headline:str | None = None
    body_test:str | None = None
    published_date:str | None = None 


    